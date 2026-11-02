"""Tkinter desktop launcher with saved-progress overview."""
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import shutil
from app import make_server, LEVELS

def main():
    root=tk.Tk()
    root.title('Rustbound • Expedition launcher')
    root.geometry('620x570')
    root.configure(bg='#101c25')
    try:
        server=make_server(0)
    except OSError as exc:
        messagebox.showerror('Cannot start Rustbound',str(exc)); root.destroy(); return
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}'
    tk.Label(root,text='RUSTBOUND',font=('Segoe UI',30,'bold'),fg='#a8edb9',bg='#101c25').pack(pady=(35,8))
    tk.Label(root,text='Small steps. Real Rust. A grand adventure.',font=('Segoe UI',12),fg='#e6e9e4',bg='#101c25').pack()
    status=tk.Label(root,font=('Segoe UI',12),fg='#e6e9e4',bg='#101c25'); status.pack(pady=24)
    tk.Label(root,text='Rust Book path · Coding · Incident workshops · MCQs',font=('Segoe UI',10),fg='#9baea9',bg='#101c25').pack()
    tk.Button(root,text='Continue expedition  →',command=lambda:webbrowser.open(url),font=('Segoe UI',14,'bold'),bg='#b8ee91',fg='#162720',relief='flat',padx=32,pady=14).pack(pady=25)
    compiler=tk.Label(root,font=('Segoe UI',10),fg='#adc5b8',bg='#101c25'); compiler.pack()
    tk.Label(root,text='Your progress is saved automatically in SQLite.\nKeep this launcher open while playing.\n\nPersonal-use code runner: Rust programs run with your\ncomputer permissions. Submit only code you trust.',font=('Segoe UI',10),fg='#9baea9',bg='#101c25',justify='center').pack(pady=22)
    tk.Button(root,text='Open the Rust Book ↗',command=lambda:webbrowser.open('https://doc.rust-lang.org/book/'),bg='#263c40',fg='white',relief='flat',padx=15,pady=8).pack()
    def refresh():
        status.config(text='Sign in in your browser to see your personal progress')
        compiler.config(text='● Rust compiler detected' if shutil.which('rustc') else 'Rust not found — install from rustup.rs and restart')
        root.after(3000,refresh)
    def close():
        server.shutdown(); server.server_close(); root.destroy()
    root.protocol('WM_DELETE_WINDOW',close)
    refresh(); root.mainloop()

if __name__=='__main__': main()
