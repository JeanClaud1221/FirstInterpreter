EOF,PLUS,MINUS,MULT,DIV,INTEGER,LPAREN,RPAREN="EOF","PLUS","MINUS","MULT","DIV","INTEGER","LPAREN","RPAREN"
class Token():
    def __init__(self,value,type):
        self.value=value
        self.type=type
    def __str__(self) -> str:
        return f"Value:{self.value},Type:{self.type}"
    def __repr__(self) -> str:
        return self.__str__()
    
class Lexer():
    def __init__(self,text:str):
        self.text=text
        self.current_pos=0
        self.current_char=self.text[self.current_pos]

    def error(self,err):
        raise Exception(err)
    
    def integer(self):
        result=""
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)

    def advance(self):
        self.current_pos+=1
        if self.current_pos>len(self.text)-1:
            self.current_char=None
        else:
            self.current_char=self.text[self.current_pos]
    
    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_space()
                continue

            if self.current_char.isdigit():
                token=Token(self.integer(),INTEGER)
                # self.advance()
                return token
            
            if self.current_char=="+":
                token=Token("+",PLUS)
                self.advance()
                return token
            
            if self.current_char=="-":
                token=Token("-",MINUS)
                self.advance()
                return token
            
            if self.current_char=="*":
                token=Token("*",MULT)
                self.advance()
                return token
            
            if self.current_char=="/":
                token=Token("/",DIV)
                self.advance()
                return token
            
            if self.current_char=="(":
                token=Token("(",LPAREN)
                self.advance()
                return token
            
            if self.current_char==")":
                token=Token(")",RPAREN)
                self.advance()
                return token
            
        return Token(None,EOF)
        
class Interpreter():
    def __init__(self,lexer:Lexer):
        self.lexer=lexer
        self.current_token=self.lexer.get_next_token()
    def error(self,err):
        raise Exception(err)
    def eat(self,token_type):
        if token_type==self.current_token.type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error("Error eating token")

    def factor(self):
        token=self.current_token
        if token.type==INTEGER:
            self.eat(INTEGER)
            return token.value
        if token.type==LPAREN:
            self.eat(LPAREN)
            result=self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result=self.factor()
        while self.current_token.type in (MULT,DIV):
            op=self.current_token
            if op.type==MULT:
                self.eat(MULT)
                result=result*self.factor()
            elif op.type==DIV:
                self.eat(DIV)
                result=result/self.factor()
        return result
    def expr(self):
        result=self.term()
        while self.current_token.type in (PLUS,MINUS):
            op=self.current_token
            if op.type==PLUS:
                self.eat(PLUS)
                result+=self.term()
            elif op.type==MINUS:
                self.eat(MINUS)
                result-=self.term()
        return result
if __name__=="__main__":
    inner=input("calc>")
    lexer=Lexer(inner)
    result=Interpreter(lexer)
    print(result.expr())


