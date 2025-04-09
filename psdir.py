# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

try:
    import sys
    sys.dont_write_bytecode = True
    
    
    from utils.dependencies import install_dependencies

    try:
        install_dependencies()
    except Exception as e:
        sys.exit(e)
        
    from controller.controller import Controller
    from core.logger import Logger
    from utils.arg_parser import parse_args
            
except KeyboardInterrupt:
    errMsg = "[!] Keyboard Interrupt detected!"
    sys.exit(errMsg)

def main():
    args = parse_args()
    
    controller = Controller(args)   
    controller.run()
    
if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        Logger.info("user interrupt")
    except Exception as e:
        Logger.error(e)
