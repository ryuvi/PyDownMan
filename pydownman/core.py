import threading
import tkinter as tk
import requests
import re

class MainPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        height = 600
        width  = 800
        self.title('PyDownMan')
        self.geometry(f'{width}x{height}')
        
        self.link = tk.StringVar()
        uLabel = tk.Label(self, text="Insert the url").pack()
        url = tk.Entry(self, textvariable=self.link)
        url.pack(fill='x')
        
        self.name = tk.StringVar()
        fnLabel = tk.Label(self, text="Insert the file name (if empty, the url one will be used)").pack()
        file_name = tk.Entry(self, textvariable=self.name)
        file_name.pack(fill='x')
        
        download_btn = tk.Button(self, text="Download", command=self.download)
        download_btn.pack()
    
    def download(self):
        if self.link.get() in ("", None):
            return -1

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

        req = requests.head(url)
        
        try:
            file_size = int(req.headers['content-length'])
        except:
            print("Invalid URL")
            return -1

        number_of_threads = 4
        part = int(int(file_size) / number_of_threads)
        fp = open(name, "wb")
        fp.write(b'\0' * file_size)
        fp.close()

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


class Header(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add download
        add_btn = tk.Button(self, text="+")
        add_btn.pack(side=tk.LEFT)
        # Resume download
        res_btn = tk.Button(self, text=">")
        res_btn.pack(side=tk.LEFT)
        # Pause download
        pas_btn = tk.Button(self, text="||")
        pas_btn.pack(side=tk.LEFT)
        # Delete download
        del_btn = tk.Button(self, text="X")
        del_btn.pack(side=tk.LEFT)
        # Show in folder
        swf_btn = tk.Button(self, text="Show")
        swf_btn.pack(side=tk.LEFT)


class List(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        


if __name__ == '__main__':
    mp = MainPage()
    mp.mainloop()