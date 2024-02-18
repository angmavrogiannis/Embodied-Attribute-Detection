from pygments import highlight 
from pygments.lexers import PythonLexer 
from pygments.formatters import SvgFormatter 
  
f = open("slide_code2.py")
code = f.read()
  
img = highlight(code, PythonLexer(),  
                SvgFormatter(style='vs'),  
                outfile="svgcode.svg")
