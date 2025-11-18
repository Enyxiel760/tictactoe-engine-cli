from src.controllers import CLIController


def main():
    # default to CLI for now
    controller = CLIController()
    controller.run()


if __name__ == "__main__":
    main()
