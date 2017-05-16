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
        xvar[:,ii+1] = rk4(xvar[:,ii],dt,w0,gd,n_var)

    df_1 = xvar[0,:]
    df_2 = xvar[1,:]

    # making the animation----------

    
    make_animation(zeit,df_1,df_2)


    #################################




def make_animation(zt,d1,d2):
    nzt = zt.size
    minval1 = min(d1)
    minval2 = min(d2)
    minval  = min(minval1,minval2)
    maxval1 = max(d1)
    maxval2 = max(d2)
    maxval  = max(maxval1,maxval2)
    fig = plt.figure()
    ax  = plt.axes(xlim=(1.1*minval,1.1*maxval) , ylim=(1.1*minval,1.1*maxval))
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$\dot\theta$")
    ax.set_aspect("equal")
    ax.grid(True,which="both")
    #lines = []
    line1, = ax.plot([],[],lw=2,color="red")
    #lines.append(line1)

    def init():
        #for line in lines:
        #    line.set_data([],[])
        #return lines
        line1.set_data([],[])
        return line1,

    def animate(i):
        xls = d1
        yls = d2
        #for lnum,line in enumerate(lines):
        #    if lnum==0:
        #        line.set_data(xls[lnum][:i], yls[lnum][:i])
        #    #if lnum==1:
        #    #    line.set_data(xls[lnum][:i], yls[lnum][:i])
        line1.set_data(xls[:i], yls[:i])
        return line1,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=nzt, interval=5, blit=True)

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
