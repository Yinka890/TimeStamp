from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
import whisper_timestamped, re

'''
def resource_path(relative_path):
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
'''

global_path = None                  

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


#ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")
#root starts here
root = Tk()
root.geometry("600x400")
root.title("Timestamp finder")

word=" "
found = []
#define function which takes path from drag and drop  space

#frame for input field and drag and drop file
frameleft = ctk.CTkFrame(root)
frameright = ctk.CTkFrame(root)
framebottom = ctk.CTkFrame(root)

frameleft.place(x= 0, y=0, relwidth=0.3, relheight=0.4)
frameright.place(relx=0.3, y=0, relwidth=0.7, relheight=0.4)
framebottom.place(x=0, rely=0.4, relwidth=1, relheight=0.6)
# input field where word is inputted to be searched
input_field = ctk.CTkEntry(frameleft, 
                           placeholder_text="Type your word here",
                           placeholder_text_color = "white")

input_field.place(relx=0.5, rely=0.5, relwidth=0.8, anchor="center")


#word should not be empty anymore
#entry_var = ctk.StringVar(value="drag you audio file here")
def get_path(event):
    global global_path
    entry_field.configure(placeholder_text=event.data)
    global_path = event.data
    print(global_path)
def copy_and_transcribe():
    output.delete("0.0", "end")
    global global_path
    global found
    word = input_field.get()
    #argument = get_path()
    found.clear()
    if word == "":
        found.append("Type a word you want to search")
        return 
    if not global_path:
        if not found:
            found.append("Drag the file you want to search")
            return 
            
    #load audio
    
    audio = whisper_timestamped.load_audio(global_path)
    #start transcribing
    model = whisper_timestamped.load_model("base")
    result = whisper_timestamped.transcribe(model, audio)
    #print
    count = 0
    # print the recognized text
    segments = result["segments"]
    segment = segments[0]
    for item in segment["words"]:
        print(item)
        if re.search(word, item["text"], re.IGNORECASE):
            count+=1
            start = item['start']
            found.append(f"found {word} at time { start}")
            break
    if not found:
        output.insert("0.0","Your word is not in the recording")
    else:
        for i in range(len(found)):
            output.insert(str(i)+".0", "".join(found[i]))
    


#drag and drop for path
entry_field = ctk.CTkEntry(frameright, 
                           placeholder_text= "drag you audio file here", 
                           placeholder_text_color = "white")

entry_field.place(relx=0.5, rely=0.6, relwidth= 0.8, relheight= 0.5, anchor="center")

#returns the results of the search
output = ctk.CTkTextbox(framebottom)
output.place(relx=0.4, rely=0.5, anchor="center")


#target = use_path_and_transcribe copy_and_transcribe()
#threading.Thread(target = copy_and_transcribe()).start()
button = ctk.CTkButton(frameleft, text="Find timestamps", 
                      command = copy_and_transcribe)
button.place(relx=0.5, rely=0.7, anchor="center")


#def update():
    #for index in range(len(timestamps)):
        #result.insert(index, timestamps[index])


entry_field.drop_target_register(DND_ALL)
entry_field.dnd_bind("<<Drop>>", get_path)

root.mainloop()

