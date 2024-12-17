# @title <p> Initialize Pendulum Class
class InvertedPendulum:
    def __init__(self,
                 m: float = 0.1,
                 M: float = 1.0,
                 L: float = 1.0,
                 g: float = 9.81,
                 d: float = 0.1,
                 t: float = 10,
                 t_sampling: float = 500,
                 x_0: float = 0,
                 theta_0: float = 0.1,
                 force_0: float = 0,
                 Q: np.ndarray = None,
                 R: np.ndarray = None):

        self.m = m
        self.M = M
        self.L = L
        self.g = g
        self.d = d
        self.t = t
        self.t_sampling = t_sampling

        self.force_0 = force_0
        self.initial = np.array([x_0, 0, theta_0, 0])

        # Matriks keadaan (state-space representation)
        self.A = np.array([
            [0, 1, 0, 0],
            [0, -self.d/self.m, -self.m*self.g/self.m, 0],
            [0, 0, 0, 1],
            [0, self.d/(self.m*self.L), (self.m+self.M)*self.g/(self.m*self.L), 0]
        ])
        self.B = np.array([[0], [-1/self.m], [0], [1/(self.m*self.L)]])

        # Matriks cost untuk LQR
        self.Q = np.diag([10, 1, 10, 1]) if Q is None else Q
        self.R = np.array([[0.1]]) if R is None else R

    def lqr(self):
        X = scipy.linalg.solve_continuous_are(self.A, self.B, self.Q, self.R)
        K = np.linalg.inv(self.R) @ self.B.T @ X
        return K

    def solve(self):
        # Hitung gain LQR
        K = self.lqr()

        def pendulum_dynamics(t, x):
            u = -K @ x + self.force_0
            dxdt = self.A @ x + self.B.flatten() * u
            return dxdt

        # Simulasi sistem
        t_span = (0, self.t)  # Rentang waktu simulasi
        t_eval = np.linspace(t_span[0], t_span[1], self.t_sampling)  # Titik waktu evaluasi
        self.solution = solve_ivp(pendulum_dynamics, t_span, self.initial, t_eval=t_eval)

    def plot(self):
        # Menjalankan simulasi
        self.solve()

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

        plt.suptitle("Simulasi Inverted Pendulum dengan LQR")
        plt.tight_layout()
        plt.show()

    def simulate(self):
      # Menjalankan simulasi
      self.solve()

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
          pendulum_x = x + self.L * np.sin(theta)
          pendulum_y = self.L * np.cos(theta)

          # Mengupdate posisi pendulum dan bola
          pendulum_line.set_data([x, pendulum_x], [0, pendulum_y])
          pendulum_ball.set_center((pendulum_x, pendulum_y))

          return cart, pendulum_line, pendulum_ball,

      # Mengatur animasi
      ani = FuncAnimation(fig, update, frames=len(self.solution.t), interval=20, blit=True)

      # Tampilkan animasi dalam format HTML
      plt.title("Simulasi Inverted Pendulum")
      plt.close(fig)
      return HTML(ani.to_jshtml())