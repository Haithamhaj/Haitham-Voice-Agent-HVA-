"""
Simple GUI Window for HVA
Shows command and response in a clean text window
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import threading


class HVAWindow:
    def __init__(self):
        self.window = None
        self.text_area = None
        self.auto_close_timer = None
        
    def create_window(self):
        """Create the main window"""
        if self.window:
            self.window.destroy()
            
        self.window = tk.Tk()
        self.window.title("🎤 Haitham Voice Agent")
        self.window.geometry("600x400")
        
        # Set window position (center of screen)
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure window
        self.window.configure(bg='#1a1a2e')
        
        # Always on top
        self.window.attributes('-topmost', True)
        
        # Create header
        header = tk.Frame(self.window, bg='#16213e', height=50)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            header,
            text="🎤 Haitham Voice Agent",
            font=('Arial', 16, 'bold'),
            bg='#16213e',
            fg='#ffffff'
        )
        title_label.pack(pady=10)
        
        # Create text area with scrollbar
        self.text_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=('Arial', 13),
            bg='#0f0f23',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            padx=20,
            pady=20
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags for styling
        self.text_area.tag_configure('user', foreground='#4facfe', font=('Arial', 13, 'bold'))
        self.text_area.tag_configure('assistant', foreground='#00f2fe', font=('Arial', 13, 'bold'))
        self.text_area.tag_configure('success', foreground='#00ff88', font=('Arial', 13))
        self.text_area.tag_configure('error', foreground='#ff6b6b', font=('Arial', 13))
        self.text_area.tag_configure('info', foreground='#a8b3ff', font=('Arial', 12, 'italic'))
        self.text_area.tag_configure('timestamp', foreground='#666666', font=('Arial', 10))
        
        # Make read-only
        self.text_area.configure(state='disabled')
        
        # Create footer with buttons
        footer = tk.Frame(self.window, bg='#16213e', height=40)
        footer.pack(fill=tk.X, padx=0, pady=0)
        
        # Pin button
        self.pin_button = tk.Button(
            footer,
            text="📌 Pin",
            command=self.toggle_pin,
            bg='#667eea',
            fg='white',
            font=('Arial', 11),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.pin_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Clear button
        clear_button = tk.Button(
            footer,
            text="🗑️ Clear",
            command=self.clear_text,
            bg='#764ba2',
            fg='white',
            font=('Arial', 11),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Close button
        close_button = tk.Button(
            footer,
            text="✕ Close",
            command=self.close_window,
            bg='#f5576c',
            fg='white',
            font=('Arial', 11),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.is_pinned = False
        
    def toggle_pin(self):
        """Toggle window pin state"""
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.pin_button.configure(text="📍 Pinned", bg='#f093fb')
            if self.auto_close_timer:
                self.auto_close_timer.cancel()
        else:
            self.pin_button.configure(text="📌 Pin", bg='#667eea')
    
    def clear_text(self):
        """Clear all text"""
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state='disabled')
    
    def close_window(self):
        """Close the window"""
        if self.auto_close_timer:
            self.auto_close_timer.cancel()
        if self.window:
            self.window.destroy()
            self.window = None
    
    def add_message(self, message_type, text, auto_close=True):
        """
        Add a message to the window
        message_type: 'user', 'assistant', 'success', 'error', 'info'
        """
        if not self.window:
            self.create_window()
        
        # Show window if hidden
        self.window.deiconify()
        self.window.lift()
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Enable editing
        self.text_area.configure(state='normal')
        
        # Add separator if not first message
        if self.text_area.get(1.0, tk.END).strip():
            self.text_area.insert(tk.END, "\n" + "─" * 60 + "\n\n")
        
        # Add timestamp
        self.text_area.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add message with appropriate styling
        if message_type == 'user':
            self.text_area.insert(tk.END, "🎤 أنت: ", 'user')
            self.text_area.insert(tk.END, f"{text}\n")
        elif message_type == 'assistant':
            self.text_area.insert(tk.END, "🤖 هيثم: ", 'assistant')
            self.text_area.insert(tk.END, f"{text}\n", 'assistant')
        elif message_type == 'success':
            self.text_area.insert(tk.END, "✅ ", 'success')
            self.text_area.insert(tk.END, f"{text}\n", 'success')
        elif message_type == 'error':
            self.text_area.insert(tk.END, "❌ ", 'error')
            self.text_area.insert(tk.END, f"{text}\n", 'error')
        elif message_type == 'info':
            self.text_area.insert(tk.END, "ℹ️  ", 'info')
            self.text_area.insert(tk.END, f"{text}\n", 'info')
        
        # Disable editing
        self.text_area.configure(state='disabled')
        
        # Auto-scroll to bottom
        self.text_area.see(tk.END)
        
        # Auto-close after 10 seconds if not pinned
        if auto_close and not self.is_pinned:
            if self.auto_close_timer:
                self.auto_close_timer.cancel()
            self.auto_close_timer = threading.Timer(10.0, self.close_window)
            self.auto_close_timer.start()
    
    def show_listening(self):
        """Show listening indicator"""
        if not self.window:
            self.create_window()
        
        self.window.deiconify()
        self.window.lift()
        
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, "\n🎤 جاري الاستماع...\n", 'info')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
    
    def show_processing(self):
        """Show processing indicator"""
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, "⚙️  جاري المعالجة...\n", 'info')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
    
    def run(self):
        """Run the GUI main loop"""
        if self.window:
            self.window.mainloop()


# Singleton instance
_window_instance = None

def get_window():
    """Get or create the singleton window instance"""
    global _window_instance
    if _window_instance is None:
        _window_instance = HVAWindow()
    return _window_instance


if __name__ == "__main__":
    # Test the window
    window = get_window()
    window.create_window()
    
    # Add some test messages
    window.add_message('user', 'احفظ ملاحظة عن الاجتماع', auto_close=False)
    window.add_message('assistant', 'تم حفظ الملاحظة بنجاح')
    window.add_message('success', 'الملاحظة: اجتماع المشروع غداً الساعة 3')
    
    window.run()
