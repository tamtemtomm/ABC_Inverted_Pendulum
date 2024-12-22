import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import display, HTML


# @title <p> Simulation class
class Simulation :
  def __init__(self, solution):
    self.solution = solution

  def plot(self, colab=False, title=None):

    if title is None : 
      title = "Simulasi Inverted Pendulum dengan LQR"
    
    # Plot hasil simulasi
    plt.figure(figsize=(8, 6))
    plt.subplot(2, 1, 1)
    plt.plot(self.solution.t, self.solution.y[0], label='Posisi Cart (x)')
    plt.plot(self.solution.t, self.solution.y[2], label='Sudut Pendulum (theta)')
    plt.xlabel('Waktu (s)')
    plt.ylabel('Posisi')
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(self.solution.t, self.solution.y[1], label='Kecepatan Cart (x_dot)')
    plt.plot(self.solution.t, self.solution.y[3], label='Kecepatan Sudut Pendulum (theta_dot)')
    plt.xlabel('Waktu (s)')
    plt.ylabel('Kecepatan')
    plt.legend()
    plt.grid()

    plt.suptitle(title)
    plt.tight_layout()
    plt.show(block=False)

  def simulate(self, L, colab=False, title=None):
    
    if title is None : 
      title = "Simulasi Inverted Pendulum"
    
    # Membuat animasi dari simulasi
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1.5, 1.5)

    # Membuat objek cart (kotak di bawah tiang)
    cart = plt.Rectangle((-0.1, -0.05), 0.2, 0.1, color='blue')
    ax.add_patch(cart)

    # Membuat garis pendulum
    pendulum_line, = ax.plot([], [], lw=2, color='black')
    # Menggambar bola di ujung pendulum
    pendulum_ball = plt.Circle((0, 0), 0.05, color='red', fill=True)
    ax.add_patch(pendulum_ball)

    def update(frame):
        # Mengupdate posisi cart dan pendulum
        x = self.solution.y[0][frame]
        theta = self.solution.y[2][frame]

        # Mengupdate posisi cart
        cart.set_xy((x - 0.1, -0.05))

        # Posisi ujung pendulum (di mana bola harus menggantung)
        pendulum_x = x + L * np.sin(theta)
        pendulum_y = L * np.cos(theta)

        # Mengupdate posisi pendulum dan bola
        pendulum_line.set_data([x, pendulum_x], [0, pendulum_y])
        pendulum_ball.set_center((pendulum_x, pendulum_y))

        return cart, pendulum_line, pendulum_ball,

    # Mengatur animasi
    ani = FuncAnimation(fig, update, frames=len(self.solution.t), interval=20, blit=True)

    # Tampilkan animasi dalam format HTML
    plt.title(title)
    
    if colab : 
      plt.close(fig)
      return HTML(ani.to_jshtml())
    
    else : 
      plt.show()