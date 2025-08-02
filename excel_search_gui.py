#!/usr/bin/env python3
"""
Excel Database Search Tool - GUI Version
Fast, user-friendly interface for searching large Excel databases
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import pandas as pd
from datetime import datetime
from search_engine import ExcelSearchEngine

class ExcelSearchGUI:
    """Main GUI application for Excel database searching"""
    
    def __init__(self):
        self.search_engine = ExcelSearchEngine()
        self.current_results = None
        self.search_timer = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Initialize the main GUI window"""
        self.root = tk.Tk()
        self.root.title("🔍 Excel Database Search Tool")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f8f9fa")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create main search tab
        self.create_search_tab()
        
        # Create file info tab
        self.create_info_tab()
        
    def create_search_tab(self):
        """Create the main search interface tab"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Search")
        
        # Configure grid
        search_frame.columnconfigure(0, weight=1)
        search_frame.rowconfigure(4, weight=1)
        
        # File selection section
        file_section = self.create_file_section(search_frame)
        file_section.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        
        # Search configuration section
        config_section = self.create_config_section(search_frame)
        config_section.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        # Search input section
        search_section = self.create_search_section(search_frame)
        search_section.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        # Status section
        status_section = self.create_status_section(search_frame)
        status_section.grid(row=3, column=0, sticky='ew', padx=10, pady=5)
        
        # Results section
        results_section = self.create_results_section(search_frame)
        results_section.grid(row=4, column=0, sticky='nsew', padx=10, pady=5)
        
        # Export section
        export_section = self.create_export_section(search_frame)
        export_section.grid(row=5, column=0, sticky='ew', padx=10, pady=(5, 10))
        
    def create_file_section(self, parent):
        """Create file selection section"""
        section = ttk.LabelFrame(parent, text="📁 File Selection", padding=10)
        section.columnconfigure(1, weight=1)
        
        # Browse button
        self.browse_btn = ttk.Button(section, text="📂 Browse Excel File", 
                                    command=self.browse_file)
        self.browse_btn.grid(row=0, column=0, padx=(0, 10))
        
        # File path label
        self.file_label = ttk.Label(section, text="No file selected", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky='w')
        
        # Load button
        self.load_btn = ttk.Button(section, text="📥 Load File", 
                                  command=self.load_file, state='disabled')
        self.load_btn.grid(row=0, column=2, padx=(10, 0))
        
        return section
    
    def create_config_section(self, parent):
        """Create search configuration section"""
        section = ttk.LabelFrame(parent, text="⚙️ Search Configuration", padding=10)
        
        # Column selection label
        ttk.Label(section, text="Select columns to search in:").grid(row=0, column=0, 
                                                                     sticky='w', pady=(0, 5))
        
        # Columns frame
        self.columns_frame = ttk.Frame(section)
        self.columns_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # Auto-select first 2 columns checkbox
        self.auto_select_var = tk.BooleanVar(value=True)
        auto_cb = ttk.Checkbutton(section, text="Auto-select first 2 columns", 
                                 variable=self.auto_select_var,
                                 command=self.on_auto_select_change)
        auto_cb.grid(row=2, column=0, sticky='w')
        
        return section
    
    def create_search_section(self, parent):
        """Create search input section"""
        section = ttk.LabelFrame(parent, text="🔎 Search", padding=10)
        section.columnconfigure(1, weight=1)
        
        # Search input
        ttk.Label(section, text="Search term:").grid(row=0, column=0, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(section, textvariable=self.search_var, 
                                     font=('Arial', 12))
        self.search_entry.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        self.search_entry.bind('<Return>', self.perform_search)
        
        # Add copy/paste support
        self.setup_search_context_menu()
        
        # Search button
        self.search_btn = ttk.Button(section, text="🔍 Search", 
                                    command=self.perform_search, state='disabled')
        self.search_btn.grid(row=0, column=2, padx=(0, 5))
        
        # Clear button
        self.clear_btn = ttk.Button(section, text="🗑️ Clear", 
                                   command=self.clear_search, state='disabled')
        self.clear_btn.grid(row=0, column=3)
        
        # Search options
        options_frame = ttk.Frame(section)
        options_frame.grid(row=1, column=0, columnspan=4, sticky='w', pady=(10, 0))
        
        self.case_sensitive_var = tk.BooleanVar()
        self.exact_match_var = tk.BooleanVar()
        self.regex_var = tk.BooleanVar()
        
        ttk.Checkbutton(options_frame, text="Case sensitive", 
                       variable=self.case_sensitive_var).grid(row=0, column=0, 
                                                              sticky='w', padx=(0, 20))
        ttk.Checkbutton(options_frame, text="Exact match", 
                       variable=self.exact_match_var).grid(row=0, column=1, 
                                                          sticky='w', padx=(0, 20))
        ttk.Checkbutton(options_frame, text="Regex search", 
                       variable=self.regex_var).grid(row=0, column=2, sticky='w')
        
        return section
    
    def create_status_section(self, parent):
        """Create status display section"""
        section = ttk.LabelFrame(parent, text="📊 Status", padding=10)
        
        self.status_label = ttk.Label(section, text="No file loaded")
        self.status_label.grid(row=0, column=0, sticky='w')
        
        return section
    
    def create_results_section(self, parent):
        """Create results display section"""
        section = ttk.LabelFrame(parent, text="📋 Search Results", padding=10)
        section.columnconfigure(0, weight=1)
        section.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        tree_frame = ttk.Frame(section)
        tree_frame.grid(row=0, column=0, sticky='nsew')
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        return section
    
    def create_export_section(self, parent):
        """Create export controls section"""
        section = ttk.Frame(parent)
        
        self.export_btn = ttk.Button(section, text="📤 Export Results", 
                                    command=self.export_results, state='disabled')
        self.export_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.result_count_label = ttk.Label(section, text="")
        self.result_count_label.grid(row=0, column=1, sticky='w')
        
        return section
    
    def create_info_tab(self):
        """Create file information tab"""
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="📋 File Info")
        
        # File info text widget
        self.info_text = tk.Text(info_frame, wrap='word', font=('Consolas', 10))
        self.info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for info text
        info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', 
                                      command=self.info_text.yview)
        info_scrollbar.pack(side='right', fill='y')
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
    def browse_file(self):
        """Open file browser to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel Database File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            initialdir="D:\\"  # Start in D drive as requested
        )
        
        if file_path:
            # Handle Unicode filenames properly
            try:
                display_name = os.path.basename(file_path)
                # Test if file is accessible
                if os.path.exists(file_path):
                    self.file_label.config(text=f"Selected: {display_name}")
                    self.search_engine.file_path = file_path
                    self.load_btn.config(state='normal')
                else:
                    messagebox.showerror("Error", f"Cannot access file: {display_name}")
            except UnicodeError:
                messagebox.showerror("Error", "Filename contains unsupported characters")
            except Exception as e:
                messagebox.showerror("Error", f"Error selecting file: {str(e)}")
    
    def load_file(self):
        """Load the selected Excel file"""
        if not hasattr(self.search_engine, 'file_path') or not self.search_engine.file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        # Show loading indicator
        self.status_label.config(text="Loading file... Please wait")
        self.load_btn.config(text="Loading...", state='disabled')
        self.root.config(cursor="wait")
        self.root.update()
        
        # Load file in separate thread to keep GUI responsive
        def load_thread():
            success, message = self.search_engine.load_file(self.search_engine.file_path)
            
            # Update GUI in main thread
            self.root.after(0, self.on_file_loaded, success, message)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def on_file_loaded(self, success, message):
        """Handle file loading completion"""
        self.root.config(cursor="")
        self.load_btn.config(text="📥 Load File", state='normal')
        
        if success:
            self.status_label.config(text=message)
            self.setup_column_selection()
            self.setup_treeview()
            self.display_initial_data()
            self.enable_search_controls()
            self.update_file_info()
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(text="File loading failed")
            messagebox.showerror("Error", message)
    
    def setup_column_selection(self):
        """Setup column selection checkboxes"""
        # Clear existing checkboxes
        for widget in self.columns_frame.winfo_children():
            widget.destroy()
        
        self.column_vars = {}
        columns = self.search_engine.df.columns.tolist()
        
        # Create checkboxes
        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            
            # Auto-select first 2 columns if enabled
            if self.auto_select_var.get() and i < 2:
                var.set(True)
            
            cb = ttk.Checkbutton(self.columns_frame, text=column, variable=var)
            cb.grid(row=i//3, column=i%3, sticky='w', padx=(0, 20), pady=2)
            
            self.column_vars[column] = var
    
    def on_auto_select_change(self):
        """Handle auto-select checkbox change"""
        if hasattr(self, 'column_vars'):
            auto_select = self.auto_select_var.get()
            columns = list(self.column_vars.keys())
            
            if auto_select:
                # Select first 2 columns
                for i, (column, var) in enumerate(self.column_vars.items()):
                    var.set(i < 2)
            else:
                # Deselect all
                for var in self.column_vars.values():
                    var.set(False)
    
    def setup_treeview(self):
        """Setup treeview columns"""
        # Clear existing
        self.tree.delete(*self.tree.get_children())
        
        columns = list(self.search_engine.df.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            # Set reasonable width
            width = min(max(len(col) * 10, 100), 200)
            self.tree.column(col, width=width, minwidth=80)
    
    def display_initial_data(self):
        """Display first 100 rows of data"""
        if self.search_engine.df is not None:
            print(f"Displaying initial data: {len(self.search_engine.df)} total rows")  # Debug
            self.display_data(self.search_engine.df.head(100))
        else:
            print("No data to display")  # Debug
    
    def display_data(self, data):
        """Display data in treeview"""
        # Clear existing
        self.tree.delete(*self.tree.get_children())
        
        if data.empty:
            self.result_count_label.config(text="No results found")
            self.current_results = data
            self.export_btn.config(state='disabled')
            return
        
        # Display limit to prevent GUI freezing
        display_limit = 1000
        display_data = data.head(display_limit)
        
        # Insert data row by row
        for _, row in display_data.iterrows():
            values = []
            for val in row:
                if pd.isna(val):
                    values.append("")
                else:
                    # Convert to string and limit length for display
                    str_val = str(val)
                    if len(str_val) > 100:  # Limit very long values
                        str_val = str_val[:97] + "..."
                    values.append(str_val)
            
            self.tree.insert("", "end", values=values)
        
        # Update result count
        total = len(data)
        if total > display_limit:
            self.result_count_label.config(
                text=f"Showing first {display_limit:,} of {total:,} results"
            )
        else:
            self.result_count_label.config(text=f"Showing {total:,} results")
        
        self.current_results = data
        self.export_btn.config(state='normal' if total > 0 else 'disabled')
    
    def enable_search_controls(self):
        """Enable search-related controls"""
        self.search_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        
        # Enable search entry
        self.search_entry.config(state='normal')
        
        # Focus on search entry for immediate use
        self.search_entry.focus_set()
    
    def get_selected_columns(self):
        """Get list of selected columns"""
        if not hasattr(self, 'column_vars'):
            return []
        
        selected = [col for col, var in self.column_vars.items() if var.get()]
        
        # If no columns selected, auto-select first 2
        if not selected and hasattr(self, 'column_vars'):
            columns = list(self.column_vars.keys())
            for i, (col, var) in enumerate(self.column_vars.items()):
                if i < 2:
                    var.set(True)
                    selected.append(col)
        
        return selected
    
    def on_search_change(self, event=None):
        """Handle search input changes for real-time search"""
        # Enable search controls if file is loaded
        if self.search_engine.df is not None:
            self.search_btn.config(state='normal')
            self.clear_btn.config(state='normal')
        
        if hasattr(self, 'search_timer') and self.search_timer:
            self.root.after_cancel(self.search_timer)
        
        # Delay search for 300ms to avoid too frequent searches
        self.search_timer = self.root.after(300, self.perform_search)
    
    def perform_search(self, event=None):
        """Perform search operation"""
        if self.search_engine.df is None:
            return
        
        search_term = self.search_var.get().strip()
        selected_columns = self.get_selected_columns()
        
        if not selected_columns:
            # Auto-select first 2 columns if none selected
            if hasattr(self, 'column_vars') and self.column_vars:
                columns = list(self.column_vars.keys())
                for i, (col, var) in enumerate(self.column_vars.items()):
                    if i < 2:
                        var.set(True)
                selected_columns = self.get_selected_columns()
            
            if not selected_columns:
                self.status_label.config(text="Please select at least one column to search in")
                return
        
        try:
            # Perform search
            results, stats = self.search_engine.search(
                search_term=search_term,
                search_columns=selected_columns,
                case_sensitive=self.case_sensitive_var.get(),
                exact_match=self.exact_match_var.get(),
                use_regex=self.regex_var.get(),
                max_results=10000  # Limit for GUI display
            )
            
            if 'error' in stats:
                self.status_label.config(text=f"Search Error: {stats['error']}")
                messagebox.showerror("Search Error", stats['error'])
                return
            
            # Update status
            if search_term:
                status_text = (f"Search: '{search_term}' | "
                              f"Found: {stats['total_results']:,} results | "
                              f"Time: {stats['search_time']:.3f}s | "
                              f"Columns: {', '.join(selected_columns)}")
            else:
                file_info = self.search_engine.get_file_info()
                status_text = (f"All data: {file_info['rows']:,} rows, "
                              f"{file_info['columns']} columns")
            
            self.status_label.config(text=status_text)
            
            # Display results
            self.display_data(results)
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            self.status_label.config(text=error_msg)
            print(f"Search error: {e}")  # Debug output
    
    def clear_search(self):
        """Clear search and show all data"""
        self.search_var.set("")
        if self.search_engine.df is not None:
            self.display_data(self.search_engine.df.head(1000))
            file_info = self.search_engine.get_file_info()
            status_text = (f"All data: {file_info['rows']:,} rows, "
                          f"{file_info['columns']} columns")
            self.status_label.config(text=status_text)
    
    def export_results(self):
        """Export current search results"""
        if self.current_results is None or self.current_results.empty:
            messagebox.showwarning("Warning", "No results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Search Results",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv")
            ]
        )
        
        if file_path:
            success, message = self.search_engine.export_results(self.current_results, file_path)
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
    
    def update_file_info(self):
        """Update the file info tab"""
        if self.search_engine.df is None:
            return
        
        file_info = self.search_engine.get_file_info()
        column_info = self.search_engine.get_column_info()
        
        info_text = f"""📊 FILE INFORMATION
{'='*50}

📁 File: {os.path.basename(self.search_engine.file_path)}
📍 Path: {self.search_engine.file_path}
📏 Size: {file_info['file_size_mb']:.2f} MB
⏱️  Load Time: {file_info['load_time']:.2f} seconds
📐 Dimensions: {file_info['rows']:,} rows × {file_info['columns']} columns
🕒 Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 COLUMN INFORMATION
{'='*50}

"""
        
        for i, col_info in enumerate(column_info, 1):
            info_text += f"{i:2d}. {col_info['name']}\n"
            info_text += f"    Type: {col_info['dtype']}\n"
            info_text += f"    Non-null: {col_info['non_null_count']:,} ({col_info['non_null_count']/file_info['rows']*100:.1f}%)\n"
            info_text += f"    Unique values: {col_info['unique_values']:,}\n"
            if col_info['sample_values']:
                info_text += f"    Sample: {', '.join(col_info['sample_values'][:3])}\n"
            info_text += "\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

    def setup_search_context_menu(self):
        """Setup right-click context menu for search entry with copy/paste"""
        # Create context menu
        self.search_context_menu = tk.Menu(self.root, tearoff=0)
        self.search_context_menu.add_command(label="📋 Paste", command=self.paste_to_search, accelerator="Ctrl+V")
        self.search_context_menu.add_command(label="📄 Copy", command=self.copy_from_search, accelerator="Ctrl+C")
        self.search_context_menu.add_command(label="✂️ Cut", command=self.cut_from_search, accelerator="Ctrl+X")
        self.search_context_menu.add_separator()
        self.search_context_menu.add_command(label="🔄 Select All", command=self.select_all_search, accelerator="Ctrl+A")
        self.search_context_menu.add_command(label="🗑️ Clear", command=self.clear_search_text)
        
        # Bind right-click to show context menu
        self.search_entry.bind('<Button-3>', self.show_search_context_menu)
        
        # Bind keyboard shortcuts
        self.search_entry.bind('<Control-v>', lambda e: self.paste_to_search())
        self.search_entry.bind('<Control-c>', lambda e: self.copy_from_search())
        self.search_entry.bind('<Control-x>', lambda e: self.cut_from_search())
        self.search_entry.bind('<Control-a>', lambda e: self.select_all_search())
    
    def show_search_context_menu(self, event):
        """Show context menu for search entry"""
        try:
            # Update menu state based on current selection
            has_selection = self.search_entry.selection_present()
            has_text = len(self.search_var.get()) > 0
            clipboard_has_text = self.has_clipboard_text()
            
            # Enable/disable menu items
            self.search_context_menu.entryconfig("📄 Copy", state="normal" if has_selection else "disabled")
            self.search_context_menu.entryconfig("✂️ Cut", state="normal" if has_selection else "disabled")
            self.search_context_menu.entryconfig("📋 Paste", state="normal" if clipboard_has_text else "disabled")
            self.search_context_menu.entryconfig("🔄 Select All", state="normal" if has_text else "disabled")
            self.search_context_menu.entryconfig("🗑️ Clear", state="normal" if has_text else "disabled")
            
            # Show menu
            self.search_context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"Context menu error: {e}")
        finally:
            self.search_context_menu.grab_release()
    
    def has_clipboard_text(self):
        """Check if clipboard contains text"""
        try:
            self.root.clipboard_get()
            return True
        except tk.TclError:
            return False
    
    def paste_to_search(self):
        """Paste text from clipboard to search entry"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                # Get current cursor position
                cursor_pos = self.search_entry.index(tk.INSERT)
                
                # If there's a selection, replace it
                if self.search_entry.selection_present():
                    start = self.search_entry.index(tk.SEL_FIRST)
                    end = self.search_entry.index(tk.SEL_LAST)
                    self.search_entry.delete(start, end)
                    cursor_pos = start
                
                # Insert clipboard text
                self.search_entry.insert(cursor_pos, clipboard_text)
                
                # Trigger search update
                self.on_search_change()
                
        except tk.TclError:
            pass  # No text in clipboard
        except Exception as e:
            print(f"Paste error: {e}")
    
    def copy_from_search(self):
        """Copy selected text from search entry to clipboard"""
        try:
            if self.search_entry.selection_present():
                selected_text = self.search_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.root.update()  # Update clipboard
        except tk.TclError:
            pass  # No selection
        except Exception as e:
            print(f"Copy error: {e}")
    
    def cut_from_search(self):
        """Cut selected text from search entry to clipboard"""
        try:
            if self.search_entry.selection_present():
                selected_text = self.search_entry.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.root.update()  # Update clipboard
                
                # Delete selected text
                start = self.search_entry.index(tk.SEL_FIRST)
                end = self.search_entry.index(tk.SEL_LAST)
                self.search_entry.delete(start, end)
                
                # Trigger search update
                self.on_search_change()
                
        except tk.TclError:
            pass  # No selection
        except Exception as e:
            print(f"Cut error: {e}")
    
    def select_all_search(self):
        """Select all text in search entry"""
        try:
            self.search_entry.select_range(0, tk.END)
        except Exception as e:
            print(f"Select all error: {e}")
    
    def clear_search_text(self):
        """Clear search entry text"""
        self.search_var.set("")
        self.clear_search()


def main():
    """Main function to start the GUI application"""
    try:
        app = ExcelSearchGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
