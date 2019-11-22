from tkinter import *
from tkinter import messagebox
from model import ONE_COMPARTMENT, TWO_COMPARTMENT
import json
import numpy as np

PATH_JSON = "constants.json"
print ("reading values from -",PATH_JSON)
with open(PATH_JSON) as f:
    args = json.load(f)
   

def plot_concentration(FLAG = "ONE COMPARTMENT"):
    t = np.linspace(0,24,1000)
    #parameters
    if FLAG[:3] == "ONE" :

        F = args['F']
        K_a = args['K_a']
        K = args['K']
        V = args['V1']
        A_O = args["INP_A"]
        tau = args["tau"]
        max_dose = args["max_dose"]

        ONE = ONE_COMPARTMENT(F, K_a, K, V, A_O, tau, max_dose)
        ONE.plot(FLAG,t)

    elif FLAG[:3] == "TWO":

        k21 = args["k21"]
        k12 = args["k12"]
        K_a = args["K_a"]
        K = args["K"]
        F = args["F"] 
        A_gut = args["INP_A"]
        V1 = args["V1"]
        V2 = args["V2"]
        A_initial  = [args["A1"], args["A2"]]
        TWO = TWO_COMPARTMENT(k21, k12, K_a, K, F, A_gut, V1, V2, A_initial, 4)
        TWO.plot(FLAG, t)
    return 0 

def close():
    sys.exit()
    # global root
    # root.quit()
    return

def sel():
   txt = var.get()
   if txt == 0:
        model = "ONE COMPARTMENT-Intravenous Bolus( SINGLE DOSE )"
   if txt == 1:
        model = "ONE COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)"
   elif txt == 2:
       model = "ONE COMPARTMENT-ORAL( SINGLE DOSE )"
   elif txt == 3:
        model = "ONE COMPARTMENT-ORAL( MULTIPLE DOSE )"
   elif txt == 4:
       model = "TWO COMPARTMENT-Intravenous Bolus( SINGLE DOSE )"
   elif txt == 5:
        model = "TWO COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)"
   elif txt == 6:
        model = "TWO COMPARTMENT-ORAL( SINGLE DOSE )"
   elif txt == 7:
        model = "TWO COMPARTMENT-ORAL( MULTIPLE DOSE )"

   messagebox.showinfo(model, "Equations solved. Press OK to see the plots!")

   plot_concentration(model)

root = Tk() 
root.geometry("1024x240+500+360") 
var = IntVar()
root.title("SELECT THE COMPARMENT MODEL")
models = [\
    "ONE COMPARTMENT-Intravenous Bolus( SINGLE DOSE )",\
    "ONE COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)",\
    "ONE COMPARTMENT-ORAL( SINGLE DOSE )",\
    "ONE COMPARTMENT-ORAL( MULTIPLE DOSE )",\
    "TWO COMPARTMENT-Intravenous Bolus( SINGLE DOSE )",\
    "TWO COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)", \
    "TWO COMPARTMENT-ORAL( SINGLE DOSE )",\
    "TWO COMPARTMENT-ORAL( MULTIPLE DOSE )", \
    "QUIT"]

for i in range(len(models)):
    button = Radiobutton(root, text = models[i], variable = var,  
                value = i, indicator = 0, 
                background = "light blue", command=sel)
    if models[i] == "QUIT":
        button = Radiobutton(root, text = models[i], variable = var,  
                    value = i, indicator = 0, 
                    background = "light blue", command=close)        
    button.pack(fill = X, ipady = 5)

label = Label(root)
label.pack()
root.mainloop()