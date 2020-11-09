from MainController import MainController

# Run this function to run the simulation
def main():
		app = MainController()
		app.geometry("1000x700")
		app.resizable(False, False)
		app.mainloop()
if __name__ == '__main__':
        main()
