import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def solution(x0,xt0,tt,w0,gd):
    # (x0,xt0,tt,w0,gd) = (theta0,omega0,time,naturalundampedfrquency,damping)
    # you should think what is dt...

    dt = 0.01

    n_time = int(tt/dt) + 1

    zeit = np.linspace(0,tt,n_time) # size of this array is n_time
    dt = zeit[1] - zeit[0]

    n_var = 2
    xvar = np.zeros((n_var,n_time))

    xvar[0,0] = x0  #initial displacement / angle
    xvar[1,0] = xt0 #initial velocity / angular velocity


    for ii in range(n_time-1):
        xnew = rk4(xvar[:,ii],dt,w0,gd,n_var)
        xvar[:,ii+1] = xnew


    df_1 = xvar[0,:]
    df_2 = xvar[1,:]



    #### find analytical solution here######
    gd2  = gd/2.0
    w1sq = gd2*gd2 - w0*w0
    # case 1: underdamped
    if w1sq<0.0:
        w1 = np.sqrt(-w1sq)
        tr2 = (xt0 + gd2*x0)/w1
        C1 = np.sqrt(x0*x0 + tr2*tr2)
        C2 = np.arctan(-tr2/x0)
        # solution: x(t) = C1*exp(-gd2*t)*cos(w1*t + C2)
        ansol1 = C1*np.exp(-gd2*zeit)*np.cos(w1*zeit + C2) #theta(t)
        ansol2 = -C1*np.exp(-gd2*zeit)*(w1*np.sin(w1*zeit+C2) + gd2*np.cos(w1*zeit+C2)) #theta_dot(t)
    # case 2: overdamped
    if w1sq>0.0:
        w1 = np.sqrt(w1sq)
        A = (xt0+(w1+gd2)*x0)/(2.0*w1)
        B = (-xt0+(w1-gd2)*x0)/(2.0*w1)
        ansol1 = A*np.exp((-gd2+w1)*zeit)+B*np.exp((-gd2-w1)*zeit) #theta(t)
        ansol2 = A*(-gd2+w1)*np.exp((-gd2+w1)*zeit) - B*(gd2+w1)*np.exp(-(gd2+w1)*zeit) #theta_dot(t)
    # case 3: critically damped
    if w1sq==0.0:
        A = x0
        B = xt0 + gd2*x0
        ansol1 = A*np.exp(-gd2*zeit) + B*zeit*np.exp(-gd2*zeit) #theta(t)
        ansol2 = -gd2*(A+B*zeit)*np.exp(-gd2*zeit) + B*np.exp(-gd2*zeit) #theta_dot(t)
    ########################################




    # making the animation----------
 
    make_animation(zeit,df_1,df_2,ansol1,ansol2)
    # pass also the analytical solution to make_animation

    #################################


def make_animation(zt,d1,d2,ans1,ans2):

    nzt = zt.size
    minval1 = min(d1)
    minval2 = min(d2)
    minval  = min(minval1,minval2)
    maxval1 = max(d1)
    maxval2 = max(d2)
    maxval  = max(maxval1,maxval2)
    fig = plt.figure()
    ax  = plt.axes(xlim=(zt[0],zt[nzt-1]) , ylim=(1.1*minval,1.1*maxval))
    #ax.set_aspect("equal")
    #ax.grid(True,which="both")
    ax.set_xlabel("Zeit")
    #ax.legend(loc="upper center")
    lines = []
    ## ask if user wants to plot analytical solution, if yes, then carry out this block; if not, skip it
    ####################################
    linm1 = ax.plot([],[],lw=1,color="black",linestyle="dotted",label="analytische loesung")[0]  # analytical solution for theta(t)
    lines.append(linm1)
    line0 = ax.plot([],[],lw=1,color="black",linestyle="dotted")[0]     # analytical solution for theta_dot(t)
    lines.append(line0)
    ####################################
    line1 = ax.plot([],[],lw=2,color="red",label=r"$x (t)$")[0]        #theta(t)
    lines.append(line1)
    line2 = ax.plot([],[],lw=2,color="blue",label=r"${\dot x} (t)$")[0]   #theta_dot(t)
    lines.append(line2)

    def init():
        for line in lines:
            line.set_data([],[])
            #line.legend()
        return lines

    def animate(i):
        xls = [zt,zt,zt,zt]
        yls = [d1,d2,ans1,ans2]
        for lnum,line in enumerate(lines):
            if lnum==0:
                line.set_data(xls[lnum], yls[lnum])
            if lnum==1:
                line.set_data(xls[lnum], yls[lnum])
            if lnum==2:
                line.set_data(xls[lnum][:i], yls[lnum][:i])
            if lnum==3:
                line.set_data(xls[lnum][:i], yls[lnum][:i])
        return lines

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nzt, interval=5, blit=True)

    plt.legend(loc="upper right",frameon=False)                              #######
    plt.show()




def rk4(xi,dt,omg0,fric,nvar):

    omg2 = omg0*omg0
    x = xi[0]
    y = xi[1]
    karr = np.zeros((nvar,4))

    karr[0,0] = y
    karr[1,0] = -omg2*x -fric*y

    karr[0,1] = y + 0.5*dt*karr[1,0]
    karr[1,1] = -omg2*(x+0.5*dt*karr[0,0]) - fric*(y + 0.5*dt*karr[1,0])

    karr[0,2] = y + 0.5*dt*karr[1,1]
    karr[1,2] = -omg2*(x+0.5*dt*karr[0,1]) - fric*(y + 0.5*dt*karr[1,1])

    karr[0,3] = y + dt*karr[1,2]
    karr[1,3] = -omg2*(x+dt*karr[0,2]) - fric*(y + dt*karr[1,2])

    k_a = (karr[:,0] + 2.0*karr[:,1] + 2.0*karr[:,2] + karr[:,3])/6.0

    xnext = xi + dt*k_a

    return xnext
