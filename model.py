import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.style.use('seaborn-bright')

class ONE_COMPARTMENT:
    """single compartment model for PK Modelling"""
    def __init__(self, F, K_a, K, V, A_O, tau, max_dose):
        self.F = F
        self.K_a = K_a
        # self.A_gut = A_gut
        self.K = K
        self.V = V
        self.A_O = A_O
        self.tau = tau
        self.max_dose = max_dose

    def A_ORAL(self, t):
        fun = self.K_a*self.F*self.A_O\
            /(self.K_a - self.K)*\
            (np.exp(-self.K*t) - np.exp(-self.K_a*t))
        return fun

    def A_bolus(self, t):
        A_Bolus =  self.A_O*np.exp(-self.K*t)
        return A_Bolus

    def C_oral(self, t):
        C_Oral = self.A_ORAL(t)/self.V 
        return C_Oral

    def C_bolus(self, t):
        C_Bolus = self.A_bolus(t)/self.V
        return C_Bolus

    def md_unit(self, n, t):
        k = self.K
        k_a = self.K_a
        tau  =self.tau
        f = 25*(np.exp(-k*(t-n*tau)) - np.exp(-k_a*(t-n*tau)))
        return f

    def val_t(self, t, tau, k, max_dose):
        max_term = int(t/tau) if int(t/tau) < max_dose else max_dose 
        cumm = self.md_unit(0,t)
        for i in range(1, max_term+1):
            cumm+=self.md_unit(i,t)
        return cumm

    def const_influx(self,t):
        F = self.F
        A_O = self.A_O
        K = self.K
        V1 = self.V
        tau = self.tau
        y = (F*A_O*(1-np.exp(-K*t)))/(tau*K*V1)
        return y

    def plot(self, flag, t):
        if flag == "ONE COMPARTMENT-Intravenous Bolus( SINGLE DOSE )":
            C = self.C_bolus(t)
            plt.title(flag, size=9)
            plt.xlabel("Hours", size=9)
            plt.ylabel("log-Concentration(mg/L)", size=9)
            plt.plot(t, np.log(C))
  
        elif flag == "ONE COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)":
            C = self.const_influx(t)
            plt.title(flag, size=9)
            plt.xlabel("Hours", size=9)
            plt.ylabel("Concentration(mg/L)", size=9)
            plt.plot(t, C)

        elif flag == "ONE COMPARTMENT-ORAL( SINGLE DOSE )":
            C = self.C_oral(t)
            plt.title(flag, size=9)
            plt.xlabel("Hours", size=9)
            plt.ylabel("Concentration(mg/L)", size=9)
            plt.plot(t, C)

        elif flag == "ONE COMPARTMENT-ORAL( MULTIPLE DOSE )":
            C = [0]*len(t)
            for j in range(t.shape[0]):
                C[j] = self.val_t(t[j], self.tau, self.K, self.max_dose )
            plt.title(flag, size=9)
            plt.xlabel("Hours", size=9)
            plt.ylabel("Concentration(mg/L)", size=9)
            plt.plot(t, C)
        plt.show()



class TWO_COMPARTMENT:

        def __init__(self, k21, k12, K_a, K, F, A_gut, V1, V2, A_initial, tau ):
            self.k12 = k12
            self.k21 = k21
            self.k_a = K_a 
            self.K = K
            self.F  = F
            self.A_gut = A_gut
            self.V1 = V1
            self.V2 = V2
            self.A1 = A_initial[0]
            self.A2 = A_initial[1]
            self.tau = tau
            self.max_dose = 3

        def solver(self, interval, A):
            A1, A2 = A[0], A[1]
            eq1 = -self.k12*A1 + self.k21*A2- self.K*A1
            eq2 = self.k12*A1 - self.k21*A2
            return [eq1, eq2]
        
        def oral_singleDose(self,interval, A):
            A1, A2, A_gut = A[0], A[1], A[2]
            eq1 = self.F*self.k_a*A_gut + self.k21*A2 - self.k12*A1 - self.K*A1
            eq2 = self.k12*A1 - self.k21*A2
            eq3 = -1*self.k_a*A_gut
            return [eq1, eq2, eq3]

        def solver_multiple(self, interval, A):
            A1, A2 = A[0], A[1]
            eq1 = -self.k12*A1 + self.k21*A2 + self.F*self.k_a*self.A_gut - self.K*A1
            eq2 = self.k12*A1 - self.k21*A2
            return [eq1, eq2]

        def const_influx(self, interval, A):
            C1, C2 = A[0], A[1]
            R_in = (self.F*self.A_gut)/self.tau
            eq1 = R_in/self.V1 + self.k21*C2- self.k12*C1-self.K*C1
            eq2 = self.k12*C1 - self.k21*C2
            return [eq1, eq2]

        def plot(self , flag, t):
            if flag == "TWO COMPARTMENT-Intravenous Bolus( SINGLE DOSE )":
                self.A1 = self.A_gut
                A = solve_ivp(self.solver, (0,25), (self.A1, self.A2), t_eval = t)
                C1 = A.y[0].flatten()/self.V1
                C2 = A.y[1].flatten()/self.V2
                # self.A_gut = 0
                plt.plot(t, np.log(C1))
                plt.title(flag, size=9)
                plt.xlabel("Hours", size=9)
                plt.ylabel("log-Concentration(mg/L)", size=9)
            
            elif flag == "TWO COMPARTMENT-ORAL( MULTIPLE DOSE )":
                
                A = solve_ivp(self.solver_multiple, (0,25), (self.A1, self.A2), t_eval = t)
                C1 = A.y[0].flatten()/self.V1
                C2 = A.y[1].flatten()/self.V2
 
                y = [0]*len(t)
                for j in range(t.shape[0]):
                    y[j] = self.val_t(t[j], self.tau, self.max_dose, C1 )
                plt.plot(t, y)
                plt.title(flag, size=9)
                plt.xlabel("Hours", size=9)
                plt.ylabel("Concentration(mg/L)", size=9)

            elif flag == "TWO COMPARTMENT-Intravenous Bolus( CONSTANT RATE INFLUX)":
                
                A = solve_ivp(self.const_influx, (0,25), (self.A1, self.A2), t_eval = t)
                C1 = A.y[0].flatten()
                C2 = A.y[1].flatten()
                plt.plot(t, C1)
                plt.title(flag, size=9)
                plt.xlabel("Hours", size=9)
                plt.ylabel("Concentration(mg/L)", size=9)                
                
            elif flag == "TWO COMPARTMENT-ORAL( SINGLE DOSE )":
                A = solve_ivp(self.oral_singleDose, (0,25), (self.A1, self.A2, self.A_gut), t_eval = t)
                C1 = A.y[0].flatten()/self.V1

                # self.A_gut = 0
                plt.plot(t, C1)
                plt.title(flag, size=9)
                plt.xlabel("Hours", size=9)
                plt.ylabel("Concentration(mg/L)", size=9)
            plt.show()

        def md_unit(self,n, t, C):
            # f = 25*(np.exp(-k*(t-n*tau)) - np.exp(-k_a*(t-n*tau)))
            tau = self.tau
            f = C[int(t-n*tau)]
            return f

        def val_t(self,t, tau, max_dose, C):
            max_term = int(t/tau) if int(t/tau) < self.max_dose else self.max_dose 
            cumm = self.md_unit(0, t, C)
            for i in range(1, max_term+1):
                cumm+=self.md_unit(i, t, C)
            return cumm