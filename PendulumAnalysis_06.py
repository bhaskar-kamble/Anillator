# this file is based on my_models_GUI_4.py.

# The "side" arguments for rb_fr.pack, screen_fr.pack and b.pack should be TOP,TOP,LEFT or LEFT,LEFT,TOP respectively
from Tkinter import *
import tkMessageBox
import pendulum_theta
import phase_theta
import animation_theta
#import ScrolledText as tkst

root = Tk( )

root.title("Pendulum analysis")

class notebook(object):
    def __init__(self,master):
        self.active_fr = None
        self.count  = 0
        self.choice = IntVar()
        self.rb_fr = Frame(master,borderwidth=2, relief=GROOVE)# this contains the "Time plot" and "Phase plot" buttons
        self.rb_fr.pack(side=TOP) # as of now side=TOP makes no difference
        self.screen_fr = Frame(master, borderwidth=2, relief=FLAT) #has "Calculating angle...initial conditions": similar label for phase plot
        self.screen_fr.pack(side=TOP)

    def __call__(self): 
        return self.screen_fr

    def add_screen(self,fr,title):
        b = Radiobutton(self.rb_fr , text=title, indicatoron=0, variable=self.choice, value=self.count, command=lambda: self.display(fr)) 
        b.pack(side=LEFT) # this ensures that the radiobuttons "Time plot" and "Phase plot" are side-by-side and not on top of each other
	if not self.active_fr:   # this if not block seems superfluous...
	    fr.pack()#(fill=BOTH, expand=1) 
	self.active_fr = fr
        self.count += 1

    def display(self, fr): 
        self.active_fr.forget( ) #if you comment this out then all the menus of DFT, STFT etc. will be exhibited.
	fr.pack(fill=BOTH, expand=1) 
	self.active_fr = fr




class Start_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Willkommen bei Anillator!\n\nMit diesem Program koennen Sie interaktive Animationen von einem eindimensionalen linearen harmonischen Oszillator mit oder ohne Reibung und mit beliebigen Anfangsbedingungen machen.\n\nDer lineare harmonische Oszillator besteht aus einer Punktmasse m, die mit einer Feder mit Federkonstante k befestigt ist. x(t) ist die Verschiebung der Masse vom Koordinatenursprung um Zeit t. xdot(t) ist die entsprechende Geschwindigkeit.\n\nUm den Oszillator zu animieren, bitte klicken Sie auf Animation und geben Sie die erforderlichen Informationen ein. Diese bestehen aus den Anfangsbedingungen x(0) und xdot(0) sowohl die Oszillatorparametren m (masse des Punktes), k (die Federkonstante) und gamma (die Reibungskonstante) als auch dem Zeitraum fuer welches Sie die Animation beobachten moechten. Am Ende klicken Sie auf Compute um die Animation zu beobachten.\n\nSie koennen auch x(t) und xdot(t) als Funktionen von Zeit beobachten. Um dieses zu tun, bitte klicken Sie auf Timeplot, geben Sie die erforderlichen Informationen ein, und klicken Sie auf Compute.\n\nUm das Phasenverhalten zu beobachten, bitte klicken Sie auf Phaseplot, geben Sie die erforderlichen Informationen ein, und klicken Sie auf Compute.\n\nWeitere Information zum Anillator Program mitsamt Erklaerungen von theoretischen Konzepten vom harmonischen Oszillator sind in den Anleitung (als pdf File) zu erhalten."


        Label(self.parent,text=choose_label,wraplength=300,width=50,height=45,relief=SUNKEN,justify=LEFT,bg="tan1").grid()
        ######################################################################################################
        #pend_pic = PhotoImage(file="./Pendulum.gif") #http://www.python-course.eu/tkinter_labels.php
        #Label(self.parent,text=choose_label,wraplength=300,width=50,height=30,relief=SUNKEN,justify=LEFT,image=pend_pic).grid()
        ######################################################################################################

        ######################################################################################################
        #tkst.ScrolledText(self.parent, text=choose_label,wraplength=400,width=50,relief=SUNKEN).grid()
        ######################################################################################################














class Animation_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Calculating x and xdot."
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))
        choose_label = "Geben Sie die Anfangsbedingungen und den Zeitraum ein"
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))

        choose_label = "x(0)"
        Label(self.parent, text=choose_label).grid()
        self.theta0 = Entry(self.parent)
        self.theta0.grid()
        self.theta0.delete(0,END)   # warum? i guess just in case there is some other text already, which is being removed thru this command
        self.theta0.insert(0,"1.0") # putting in a default value

        choose_label = "xdot(0)"
        Label(self.parent, text=choose_label).grid()
        self.omega0 = Entry(self.parent)
        self.omega0.grid()
        self.omega0.delete(0,END)
        self.omega0.insert(0,"0.0")
        
        choose_label = "time"
        Label(self.parent, text=choose_label).grid()
        self.time = Entry(self.parent)
        self.time.grid()
        self.time.delete(0,END)
        self.time.insert(0,"60.0")

        choose_label = "Frequenz des Oszillators"
        Label(self.parent, text=choose_label).grid()
        self.w_osc = Entry(self.parent)
        self.w_osc.grid()
        self.w_osc.delete(0,END)
        self.w_osc.insert(0,"1.0")

        choose_label = "Reibungskonstante"
        Label(self.parent, text=choose_label).grid()
        self.damp = Entry(self.parent)
        self.damp.grid()
        self.damp.delete(0,END)
        self.damp.insert(0,"0.1")

        # Button to compute theta and omega
        self.compute = Button(self.parent,text="Compute",command=lambda:self.compute_animation())
        self.compute.grid()

    def compute_animation(self):
        try:
            initial_theta = float(self.theta0.get())
            initial_omega = float(self.omega0.get())
            zeit          = float(self.time.get())
            frequenz      = float(self.w_osc.get())
            gamma         = float(self.damp.get())

            #tkMessageBox.showinfo(message="We will now calculate theta and omega")

            animation_theta.solution(initial_theta,initial_omega,zeit,frequenz,gamma) ######## make this file!

        except ValueError as errorMessage:
	    tkMessageBox.showerror("Input values error",errorMessage)



class Timeplot_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Calculating x and xdot."
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))
        choose_label = "Geben Sie die Anfangsbedingungen und den Zeitraum ein"
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))

        choose_label = "x(0)"
        Label(self.parent, text=choose_label).grid()
        self.theta0 = Entry(self.parent)
        self.theta0.grid()
        self.theta0.delete(0,END)   # warum? i guess just in case there is some other text already, which is being removed thru this command
        self.theta0.insert(0,"1.0") # putting in a default value

        choose_label = "xdot(0)"
        Label(self.parent, text=choose_label).grid()
        self.omega0 = Entry(self.parent)
        self.omega0.grid()
        self.omega0.delete(0,END)
        self.omega0.insert(0,"0.0")
        
        choose_label = "time"
        Label(self.parent, text=choose_label).grid()
        self.time = Entry(self.parent)
        self.time.grid()
        self.time.delete(0,END)
        self.time.insert(0,"60.0")

        choose_label = "Frequenz des Oszillators"
        Label(self.parent, text=choose_label).grid()
        self.w_osc = Entry(self.parent)
        self.w_osc.grid()
        self.w_osc.delete(0,END)
        self.w_osc.insert(0,"1.0")

        choose_label = "Reibungskonstante"
        Label(self.parent, text=choose_label).grid()
        self.damp = Entry(self.parent)
        self.damp.grid()
        self.damp.delete(0,END)
        self.damp.insert(0,"0.1")

        # Button to compute theta and omega
        self.compute = Button(self.parent,text="Compute",command=lambda:self.compute_theta_dot())
        self.compute.grid()

    def compute_theta_dot(self):
        try:
            initial_theta = float(self.theta0.get())
            initial_omega = float(self.omega0.get())
            zeit          = float(self.time.get())
            frequenz      = float(self.w_osc.get())
            gamma         = float(self.damp.get())

            #tkMessageBox.showinfo(message="We will now calculate theta and omega")

            pendulum_theta.solution(initial_theta,initial_omega,zeit,frequenz,gamma)

        except ValueError as errorMessage:
	    tkMessageBox.showerror("Input values error",errorMessage)






class Phaseplot_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Calculating phase plot."
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))
        choose_label = "Give initial conditions and time"
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))

        choose_label = "theta(0)"
        Label(self.parent, text=choose_label).grid()
        self.theta0 = Entry(self.parent)
        self.theta0.grid()
        self.theta0.delete(0,END)   # warum? i guess just in case there is some other text already, which is being removed thru this command
        self.theta0.insert(0,"1.0") # putting in a default value

        choose_label = "omega(0)"
        Label(self.parent, text=choose_label).grid()
        self.omega0 = Entry(self.parent)
        self.omega0.grid()
        self.omega0.delete(0,END)
        self.omega0.insert(0,"0.0")

        choose_label = "time"
        Label(self.parent, text=choose_label).grid()
        self.time = Entry(self.parent)
        self.time.grid()
        self.time.delete(0,END)
        self.time.insert(0,"60.0")

        choose_label = "Frequency of oscillator"
        Label(self.parent, text=choose_label).grid()
        self.w_osc = Entry(self.parent)
        self.w_osc.grid()
        self.w_osc.delete(0,END)
        self.w_osc.insert(0,"1.0")

        choose_label = "Damping constant"
        Label(self.parent, text=choose_label).grid()
        self.damp = Entry(self.parent)
        self.damp.grid()
        self.damp.delete(0,END)
        self.damp.insert(0,"0.1")

        # Button to compute phase space plot
        self.compute = Button(self.parent,text="Compute",command=lambda:self.compute_phaseplot())#None)
        self.compute.grid()

    def compute_phaseplot(self):
        try:
            initial_theta = float(self.theta0.get())
            initial_omega = float(self.omega0.get())
            zeit          = float(self.time.get())
            frequenz      = float(self.w_osc.get())
            gamma         = float(self.damp.get())

            #tkMessageBox.showinfo(message="We will now calculate the phase plot")

            phase_theta.solution(initial_theta,initial_omega,zeit,frequenz,gamma)

        except ValueError as errorMessage:
	    tkMessageBox.showerror("Input values error",errorMessage)





nb = notebook(root) # an instance of "notebook" class created



f0 = Frame(nb())
nb.add_screen(f0,"Start")
anfang = Start_frame(f0)



fa0 = Frame(nb())
nb.add_screen(fa0,"Animation")
animat = Animation_frame(fa0)



f1 = Frame(nb()) #Frame(nb( ))#screen_fr returned - if u dont frame this all will be shown
dft = Timeplot_frame(f1)  # has now been attached the label "Calculating angle and..."
nb.add_screen(f1, "Time plot") # f1 here is NOT the frame containing the radiobuttons "Time plot" and "Phase plot". It is the frame containing hte labels "Calculating angle...give inital conditions".  But this add_screen adds the "Time plot" and "Phase plot" to the rb_fr frame. "f1" here goes to the fr argument in command=lambda:self.display(fr) in the add_screen function, i.e. f1, which contains "Calculating angle as function of time...give initial conditions" will be packed and displayed when "Time plot" is pressed.



f2 = Frame(nb( ))#Frame(nb( )) 
nb.add_screen(f2, "Phase plot")
stft = Phaseplot_frame(f2)


nb.display(f0)

root.geometry('+0+0')
root.mainloop( )
