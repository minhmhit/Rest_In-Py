import tkinter as tk
from tkinter import ttk, Toplevel, Label, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, date # Import date as well
import locale
import calendar # Import calendar module for month names

from view.models import CustomerInfo # Assuming this exists and has attributes

# --- Define colors --- (Keep consistent with other files)
COLOR_PRIMARY_BLUE = "#3B82F6"      # Màu xanh dương chính
COLOR_PRIMARY_BLUE_DARK = "#0056b3" # Darker blue for hover/active
COLOR_ACCENT_GREEN = "#28a745"      # Green for success actions
COLOR_ACCENT_RED = "#dc3545"        # Red for danger actions
COLOR_ACCENT_TEAL = "#17a2b8"       # Teal for info/export actions
COLOR_BACKGROUND_LIGHT = "#eef2f7"  # Light background for main frame
COLOR_FRAME_BACKGROUND = "#f8f9fa"  # Slightly gray background for panels/frames
COLOR_MAIN_PANEL_BG = "#ffffff"     # White background for main content areas
COLOR_TEXT_DARK = "#333333"    # Dark gray for primary text
COLOR_TEXT_MEDIUM = "#555555" # Medium gray for secondary text/frame titles
COLOR_BORDER_GRAY = "#cccccc"       # Light gray border
COLOR_WHITE = "#ffffff" # White color
COLOR_TEXT_PLACEHOLDER = "gray" # Gray color for placeholder text

# --- Currency Formatting ---
try:
    # Set locale for Vietnamese currency formatting
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
except locale.Error:
    try:
        # Fallback for Windows
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
    except locale.Error:
        print("Warning: Could not set Vietnamese locale for currency formatting in RevenueChart.")
        # Define a basic formatting function if locale fails
        def format_currency(amount):
            # Basic format: add commas for thousands, round to 0 decimals, add VND
            return f"{amount:,.0f}".replace(",", ".") + " VND"
    else:
        # Use locale.currency if fallback worked
        def format_currency(amount):
            return locale.currency(amount, grouping=True, symbol=" VND")
else:
     # Use locale.currency if primary locale worked
     def format_currency(amount):
        return locale.currency(amount, grouping=True, symbol=" VND")

# Ensure format_currency is defined even if all locale settings fail
if 'format_currency' not in locals():
     def format_currency(amount):
            return f"{amount:,.0f}".replace(",", ".") + " VND"
# --- End Currency Formatting ---

class RevenueChart(tk.Frame):
    # Receive customer_list from the parent (App)
    def __init__(self, parent, customer_list):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT) # Use consistent background

        # Store the received customer list
        self.customer_list = customer_list

        # Define price per day for room types (assuming this is fixed or accessible)
        self.price_per_day = {"VIP": 400000, "Thường": 250000} # Example prices

        # Dictionaries to store processed data (will be populated in process_revenue_data)
        self.revenue_by_year = {}
        self.customer_count_by_year = {}
        self.province_revenue_by_year = {}
        self.revenue_by_month_year = {} # New: Revenue by Month/Year (format "YYYY-MM")

        self.province_colors = {} # Store province and color mapping for the chart


        # Create the widgets (Notebook, frames for tabs)
        self.create_widgets()

        # Process data and update charts after widgets are ready
        self.process_revenue_data()
        self.update_charts()


    def _process_date_input_to_datetime(self, raw_date_value):
         """Converts raw date input (string or datetime) to a datetime object or None."""
         if isinstance(raw_date_value, datetime):
              return raw_date_value # Already a datetime object
         elif isinstance(raw_date_value, date): # Handle date objects too
              # Combine date object with min time to make it a datetime object
              return datetime.combine(raw_date_value, datetime.min.time())
         elif isinstance(raw_date_value, str) and raw_date_value.strip(): # Check for non-empty string after stripping whitespace
              try:
                   # Try parsing from YYYY-MM-DD string
                   return datetime.strptime(raw_date_value.strip(), "%Y-%m-%d") # Strip whitespace before parsing
              except ValueError:
                   # If YYYY-MM-DD fails, try other common formats if necessary,
                   # but for consistency, we expect YYYY-MM-DD.
                   print(f"Warning: Could not parse date string '{raw_date_value.strip()}'. Expected YYYY-MM-DD.")
                   return None
         else:
              return None # None, empty string, or other types are treated as no date


    # --- Process Customer Data to Aggregate Revenue ---
    def process_revenue_data(self):
        """
        Processes the customer list to calculate revenue and customer counts
        aggregated by year, month/year, and province/year.
        Populates self.revenue_by_year, self.customer_count_by_year,
        self.province_revenue_by_year, self.revenue_by_month_year.
        """
        # Clear previous data before processing
        self.revenue_by_year.clear()
        self.customer_count_by_year.clear()
        self.province_revenue_by_year.clear()
        self.revenue_by_month_year.clear()

        today = datetime.today()

        if not self.customer_list:
            print("No customer data to process for revenue charts.")
            return # Exit if list is empty

        for customer in self.customer_list:
            # Get check-in date, province, and room type from CustomerInfo object
            raw_checkin_date = getattr(customer, 'checkin_date', None)
            province = getattr(customer, 'country', 'Unknown') # Use 'country' for province/city, default to 'Unknown'
            room_type = getattr(customer, 'room_type', None)

            # Process the check-in date into a datetime object
            checkin_dt = self._process_date_input_to_datetime(raw_checkin_date)

            # Ensure we have a valid check-in date and known room type
            if checkin_dt and room_type in self.price_per_day:
                # Calculate duration in days (from check-in to today)
                duration = (today - checkin_dt).days

                # Only consider non-negative duration (customer checked in before or on today)
                if duration >= 0:
                    # Get the price per day for the room type, default to 0 if not found
                    price = self.price_per_day.get(room_type, 0)
                    # Calculate revenue for this customer's stay duration
                    revenue = duration * price

                    # --- Aggregate Data ---

                    # Get year and month for aggregation
                    year = checkin_dt.year
                    month_year = checkin_dt.strftime("%Y-%m") # Format as "YYYY-MM"

                    # 1. Total Revenue by Year
                    if year not in self.revenue_by_year:
                         self.revenue_by_year[year] = 0
                    self.revenue_by_year[year] += revenue

                    # 2. Customer Count by Year (Counting check-ins per year)
                    # This counts how many check-ins happened each year
                    if year not in self.customer_count_by_year:
                         self.customer_count_by_year[year] = 0
                    self.customer_count_by_year[year] += 1 # Count each customer/check-in event

                    # 3. Revenue by Province by Year
                    if year not in self.province_revenue_by_year:
                         self.province_revenue_by_year[year] = {}
                    if province not in self.province_revenue_by_year[year]:
                         self.province_revenue_by_year[year][province] = 0
                    self.province_revenue_by_year[year][province] += revenue

                    # 4. Revenue by Month/Year
                    if month_year not in self.revenue_by_month_year:
                        self.revenue_by_month_year[month_year] = 0
                    self.revenue_by_month_year[month_year] += revenue

        print("Revenue data processed successfully.")

    # --- Create Widgets (Notebook, Tab Frames) ---
    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Add padding around the notebook

        # --- Style for the Frames *inside* the Notebook tabs ---
        style = ttk.Style()
        style.configure("ChartFrame.TFrame", background=COLOR_MAIN_PANEL_BG) # Use white background


        # --- Frame for Total Revenue Chart ---
        self.revenue_frame = ttk.Frame(self.notebook, style="ChartFrame.TFrame") # Apply style
        self.notebook.add(self.revenue_frame, text="Tổng Doanh Thu (Năm)") # Use self. for instance attribute

        # --- Frame for Customer Growth Chart ---
        self.customer_frame = ttk.Frame(self.notebook, style="ChartFrame.TFrame") # Apply style
        self.notebook.add(self.customer_frame, text="Tăng Trưởng Khách Hàng (Năm)") # Use self. for instance attribute

        # --- Frame for Revenue by Province Chart ---
        self.province_frame = ttk.Frame(self.notebook, style="ChartFrame.TFrame") # Apply style
        self.notebook.add(self.province_frame, text="Doanh Thu theo Tỉnh (Năm)") # Use self. for instance attribute

        # --- Frame for Monthly Revenue Chart ---
        self.monthly_revenue_frame = ttk.Frame(self.notebook, style="ChartFrame.TFrame") # Apply style
        self.notebook.add(self.monthly_revenue_frame, text="Doanh Thu theo Tháng") # Use self. for instance attribute

        # Style the button consistently
        button_font = ("Arial", 10, "bold")
        button_pady = 5
        button_padx = 10

        self.color_button = tk.Button( # Use tk.Button for more styling control
             self.province_frame, text="Hiển thị Chú giải Tỉnh", command=self.show_province_colors,
             font=button_font, bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE,
             activebackground=COLOR_PRIMARY_BLUE_DARK, activeforeground=COLOR_WHITE,
             relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2"
        )
        self.color_button.pack(pady=10) # Add some padding below the button


    # --- Update Charts after Data Processing ---
    def update_charts(self):
        """Clears previous charts and draws new ones based on processed data."""
        # Clear previous charts from frames if they exist
        for widget in self.revenue_frame.winfo_children(): widget.destroy()
        for widget in self.customer_frame.winfo_children(): widget.destroy()
        for widget in self.province_frame.winfo_children(): widget.destroy()
        for widget in self.monthly_revenue_frame.winfo_children(): widget.destroy()


        # Get sorted years and month-years
        years = sorted(self.revenue_by_year.keys())
        month_years = sorted(self.revenue_by_month_year.keys())


        # Draw charts if data is available
        if years:
            # Data for yearly charts
            yearly_revenue_data = [self.revenue_by_year.get(year, 0) for year in years]
            yearly_customer_data = [self.customer_count_by_year.get(year, 0) for year in years]

            self.create_revenue_chart(self.revenue_frame, years, yearly_revenue_data)
            self.create_customer_chart(self.customer_frame, years, yearly_customer_data)
            self.create_province_revenue_chart(self.province_frame, years, self.province_revenue_by_year)

        if month_years:
            # Data for monthly chart
            monthly_revenue_values = [self.revenue_by_month_year.get(my, 0) for my in month_years]
            self.create_monthly_revenue_chart(self.monthly_revenue_frame, month_years, monthly_revenue_values)

        else:
             # Display a message if no data
             no_data_label = tk.Label(
                  self.notebook, text="Không có dữ liệu doanh thu để hiển thị.",
                  font=("Arial", 12), fg=COLOR_TEXT_MEDIUM, bg=COLOR_BACKGROUND_LIGHT
             )
             no_data_label.pack(pady=20, fill=tk.BOTH, expand=True)



    # --- Chart Creation Methods ---

    def create_revenue_chart(self, parent, years, revenue_data):
        """Creates and embeds the Total Revenue by Year bar chart."""
        # Clear previous plot (if any) and create new figure/axes
        plt.close('all') # Close all existing plot figures
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=COLOR_MAIN_PANEL_BG) # Use white background for figure patch

        # Create the bar chart
        bars = ax.bar(years, revenue_data, color=COLOR_PRIMARY_BLUE) # Use primary blue for bars

        # Add revenue values on top of bars
        for bar in bars:
            yval = bar.get_height()
            # Format value for display (optional, depends on scale)
            display_value = format_currency(yval)
            # Adjust vertical position of text
            va = 'bottom' if yval > 0 else 'top'
            ax.text(bar.get_x() + bar.get_width()/2, yval, display_value, va=va, ha='center', fontsize=8, color=COLOR_TEXT_DARK)


        # Style the chart elements
        ax.set_xlabel("Năm", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_ylabel("Tổng Doanh Thu", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_title("Tổng Doanh Thu qua các Năm", fontsize=14, color=COLOR_TEXT_DARK, pad=15) # Add padding below title
        ax.tick_params(axis='x', colors=COLOR_TEXT_MEDIUM, labelsize=10) # Style x ticks
        ax.tick_params(axis='y', colors=COLOR_TEXT_MEDIUM, labelsize=10) # Style y ticks
        ax.spines['top'].set_visible(False) # Hide top spine
        ax.spines['right'].set_visible(False) # Hide right spine
        ax.set_facecolor(COLOR_MAIN_PANEL_BG) # Use white background for axes


        # Embed the plot in the Tkinter parent frame
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Add padding around the chart widget
        canvas.draw()


    def create_customer_chart(self, parent, years, customer_data):
        """Creates and embeds the Customer Growth by Year line chart."""
        plt.close('all') # Close existing figures
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=COLOR_MAIN_PANEL_BG) # Use white background

        # Create the line chart
        line, = ax.plot(years, customer_data, marker='o', linestyle='-', color=COLOR_ACCENT_GREEN) # Use accent green for line

        # Add customer count values next to markers
        for i, year in enumerate(years):
            count = customer_data[i]
            ax.text(year, count, str(count), ha='center', va='bottom', fontsize=8, color=COLOR_TEXT_DARK)


        # Style the chart elements
        ax.set_xlabel("Năm", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_ylabel("Số lượng Khách hàng", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_title("Tăng trưởng Khách hàng qua các Năm (Lượt Check-in)", fontsize=14, color=COLOR_TEXT_DARK, pad=15) # Add padding
        ax.tick_params(axis='x', colors=COLOR_TEXT_MEDIUM, labelsize=10)
        ax.tick_params(axis='y', colors=COLOR_TEXT_MEDIUM, labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='--', alpha=0.7, color=COLOR_BORDER_GRAY) # Add grid
        ax.set_facecolor(COLOR_MAIN_PANEL_BG) # Use white background


        # Embed the plot
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()


    def create_province_revenue_chart(self, parent, years, province_revenue_data):
        """Creates and embeds the Revenue by Province by Year grouped bar chart."""
        plt.close('all') # Close existing figures
        fig, ax = plt.subplots(figsize=(10, 7), facecolor=COLOR_MAIN_PANEL_BG) # Use white background

        # Get all unique provinces and sort them
        all_provinces = sorted(list(set(p for year_data in province_revenue_data.values() for p in year_data.keys())))
        num_provinces = len(all_provinces)

        if num_provinces == 0 or not years:
             print("No province revenue data or years to plot.")
             # Display a message inside the frame if no data
             no_data_label = tk.Label(
                  parent, text="Không có dữ liệu doanh thu theo tỉnh để hiển thị.",
                  font=("Arial", 12), fg=COLOR_TEXT_MEDIUM, bg=COLOR_MAIN_PANEL_BG
             )
             no_data_label.pack(pady=20, fill=tk.BOTH, expand=True)
             # Hide the color button if no data
             if self.color_button:
                  self.color_button.pack_forget()
             plt.close(fig) # Close the empty figure
             return

        colors = plt.cm.get_cmap('tab10', max(num_provinces, 10)) # Use tab10, ensure at least 10 colors if num_provinces is small

        # Assign a color and position index to each province
        province_positions = {province: i for i, province in enumerate(all_provinces)}
        color_map = {province: colors(i) for i, province in enumerate(all_provinces)}
        self.province_colors = color_map # Store the map for the legend button


        bar_width = 0.8 / max(num_provinces, 1) # Avoid division by zero if no provinces

        # Plot bars for each province within each year
        for i, year in enumerate(years):
            province_data_this_year = province_revenue_data.get(year, {})
            for province in all_provinces: # Iterate through all provinces for consistent bars
                revenue = province_data_this_year.get(province, 0) # Get revenue for this province/year, default to 0
                position = province_positions[province]
                # Calculate x position for the bar within the year's group
                x_pos = i + (position - num_provinces / 2) * bar_width + bar_width / 2 # Center the group around the year tick

                # Plot the bar
                # Add label only for the first year for the legend
                label = province if year == years[0] else ""
                ax.bar(x_pos, revenue, width=bar_width, label=label, color=color_map[province])

                # Add revenue value on top of the bar if non-zero (optional)
                if revenue > 0:
                    ax.text(x_pos, revenue, format_currency(revenue), ha='center', va='bottom', fontsize=7, color=COLOR_TEXT_DARK, rotation=90) # Rotate text


        # Style the chart elements
        ax.set_xlabel("Năm", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_ylabel("Doanh Thu", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_title("Doanh thu theo Tỉnh qua các Năm", fontsize=14, color=COLOR_TEXT_DARK, pad=15) # Add padding

        # Set x ticks to be at the center of the year groups
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels(years, fontsize=10, color=COLOR_TEXT_MEDIUM)
        ax.tick_params(axis='y', colors=COLOR_TEXT_MEDIUM, labelsize=10)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add legend
        # Adjust legend position if it overlaps with the plot
        ax.legend(title="Tỉnh", fontsize=9, loc='upper left', bbox_to_anchor=(1, 1))

        ax.set_facecolor(COLOR_MAIN_PANEL_BG) # Use white background for axes
        fig.patch.set_facecolor(COLOR_MAIN_PANEL_BG) # Use white background for figure patch
        fig.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend if on the side


        # Embed the plot
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()


    def create_monthly_revenue_chart(self, parent, month_years, revenue_data):
        """Creates and embeds the Revenue by Month/Year line chart."""
        plt.close('all') # Close existing figures
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=COLOR_MAIN_PANEL_BG) # Use white background

        # Create the line chart
        line, = ax.plot(month_years, revenue_data, marker='o', linestyle='-', color=COLOR_ACCENT_TEAL) # Use accent teal

        # Style the chart elements
        ax.set_xlabel("Tháng/Năm", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_ylabel("Doanh Thu", fontsize=12, color=COLOR_TEXT_DARK)
        ax.set_title("Doanh Thu theo Tháng/Năm", fontsize=14, color=COLOR_TEXT_DARK, pad=15) # Add padding

        # Improve x-axis tick display for many months
        ax.set_xticks(month_years) # Set ticks at each month/year
        ax.set_xticklabels(month_years, rotation=45, ha='right', fontsize=9, color=COLOR_TEXT_MEDIUM) # Rotate and align labels

        ax.tick_params(axis='y', colors=COLOR_TEXT_MEDIUM, labelsize=10)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='--', alpha=0.7, color=COLOR_BORDER_GRAY) # Add grid
        ax.set_facecolor(COLOR_MAIN_PANEL_BG) # Use white background


        # Adjust layout to prevent labels overlapping
        fig.tight_layout()

        # Embed the plot
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()


    # --- Show Province Color Legend ---
    def show_province_colors(self):
        if not self.province_colors:
            messagebox.showinfo("Thông tin", "Không có dữ liệu tỉnh/thành phố để hiển thị chú giải.")
            return

        top = Toplevel(self, bg=COLOR_BACKGROUND_LIGHT) # Consistent background for pop-up
        top.title("Chú giải Màu sắc theo Tỉnh")
        top.transient(self.winfo_toplevel()) # Keep on top of main window
        top.grab_set() # Block interaction with parent windows

        padding_frame = tk.Frame(top, bg=COLOR_BACKGROUND_LIGHT, padx=10, pady=10) # Padding inside pop-up
        padding_frame.pack(fill="both", expand=True)

        title_label = tk.Label(padding_frame, text="Màu sắc các Tỉnh/Thành phố:", font=("Arial", 12, "bold"), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK)
        title_label.pack(pady=(0, 10))

        # Display each province and its color
        for province, color_tuple in self.province_colors.items():
            # Convert Matplotlib color tuple (RGB 0-1) to hex (#RRGGBB)
            color_hex = '#%02x%02x%02x' % (int(color_tuple[0]*255), int(color_tuple[1]*255), int(color_tuple[2]*255))

            # Use a Frame for each row (color block + label)
            frame = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT) # Row frame
            frame.pack(fill=tk.X, pady=2) # Pack row frames

            # Color block label
            color_label = tk.Label(frame, text="", bg=color_hex, width=3, relief=tk.SOLID, bd=1) # Use tk.Label for more styling, add border
            color_label.pack(side=tk.LEFT, padx=5)

            # Province name label
            province_label = tk.Label(frame, text=f"{province}", bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK, font=("Arial", 10)) # Province name
            province_label.pack(side=tk.LEFT, padx=2)
