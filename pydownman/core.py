import threading
import customtkinter as tk
import requests
import re
import os

class MainPage(tk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        height = 600
        width  = 800
        self.title('PyDownMan')
        self.geometry(f'{width}x{height}')
        
        self.link = tk.StringVar()
        uLabel = tk.CTkLabel(self, text="Insert the url").pack()
        url = tk.CTkEntry(self, textvariable=self.link)
        url.pack(fill='x', padx=10, pady=10)
        
        self.name = tk.StringVar()
        fnLabel = tk.CTkLabel(self, text="Insert the file name (if empty, the url one will be used)").pack()
        file_name = tk.CTkEntry(self, textvariable=self.name)
        file_name.pack(fill='x', padx=10, pady=10)
        
        download_btn = tk.CTkButton(self, text="Download", command=self.download)
        download_btn.pack()
        
        add_btn = tk.CTkButton(self, text="+", command=self.open_add)
        add_btn.place(relx=0.75, rely=0.75)
    
    def open_add(self):
        add = AddLink()
        self.link.set(add.get_url())
        self.download()
    
    def download(self):
        if self.link.get() in ("", None):
            return -1
        
        self.check_download_folder()

        url = self.link.get()
        urls_ext = [".com",".org",".net",".int",".edu",".gov",".mil"]

        if self.name.get() in ("", None):
            link_sections = url.split("/")
            for section in link_sections:
                name = re.search('\.[0-9a-z]+$', section)
                if name is not None:
                    name = name.group()
                if name not in urls_ext and name is not None:
                    name = section
                    break
        else:
            name = self.name.get()

        req = requests.head(url)
        
        try:
            file_size = int(req.headers['content-length'])
        except:
            print("Invalid URL")
            return -1

        number_of_threads = 4
        part = int(int(file_size) / number_of_threads)
        with open(f"downloads/{name}", "wb") as f:
            f.write(b'\0' * file_size)

        for i in range(number_of_threads):
            start = part * i
            end = start + part
            t = threading.Thread(target=self.handler,
                                 kwargs={'start': start, 'end': end, 'url': url, 'filename': name},
                                 daemon=True)
            t.start()

        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        print(f"{name} downloaded")


    def handler(self, start, end, url, filename):
        headers = {'Range': f'bytes={start}-{end}'}
        r = requests.get(url, headers=headers, stream=True)
        with open(filename, "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
            
    def check_download_folder(self):
        if not os.path.isdir("downloads/"):
            os.mkdir("downloads")


class AddLink(tk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Adicionar")
        
        self.link = tk.StringVar()
        entry = tk.CTkEntry(self, textvariable=self.link)
        entry.pack(expand=True, fill='x')
        
        frame = tk.CTkFrame(self)
        frame.pack(expand=True, fill='x')
        cancel = tk.CTkButton(frame, text="Cancel", command=self.destroy)
        cancel.pack(side=tk.RIGHT)
        add = tk.CTkButton(frame, text="Ok", command=self.destroy)
        add.pack(side=tk.RIGHT)
    
    def get_url(self):
        return self.link.get()

# class Header(tk.Frame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add download
#         add_btn = tk.Button(self, text="+")
#         add_btn.pack(side=tk.LEFT)
#         # Resume download
#         res_btn = tk.Button(self, text=">")
#         res_btn.pack(side=tk.LEFT)
#         # Pause download
#         pas_btn = tk.Button(self, text="||")
#         pas_btn.pack(side=tk.LEFT)
#         # Delete download
#         del_btn = tk.Button(self, text="X")
#         del_btn.pack(side=tk.LEFT)
#         # Show in folder
#         swf_btn = tk.Button(self, text="Show")
#         swf_btn.pack(side=tk.LEFT)


# class List(tk.Frame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        


if __name__ == '__main__':
    mp = MainPage()
    mp.mainloop()