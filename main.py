import sys
from lib.app import Application
from lib.argparser import Argparser


def main():
    parser = Argparser()
    arguments = parser.parse_args()

    app = Application(arguments)
    result = app.run()
    print()
    return result


if __name__ == "__main__":
    sys.exit(main())
