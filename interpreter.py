# input= "123+4-5+81"
EOF,INTEGER,PLUS,MINUS,MULT,DIV="EOF","INTEGER","PLUS","MINUS","MULT","DIV"
class Token():
    def __init__(self,value,type):
        self.value=value
        self.type=type
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"Value:{self.value} Type:{self.type}"

class Lexer():
    def __init__(self,text:str):
        self.text=text
        self.pos=0
        self.current_char=self.text[self.pos]
        # self.current_token=None
    def error(self):
        raise Exception("Lexer error")
    def advance(self):
        self.pos+=1
        if self.pos>len(self.text)-1:
            self.current_char=None
        else:
            self.current_char=self.text[self.pos]
    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result=""
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)
    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_white_space()
                continue

            if self.current_char=="+":
                token=Token("+",PLUS)
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
            
            if self.current_char=="-":
                token=Token("-",MINUS)
                self.advance()
                return token
            
            if self.current_char.isdigit():
                token=Token(self.integer(),INTEGER)
                # self.advance()
                return token
            
        return Token("EOF",EOF)

class Intepreter():
    def __init__(self,lexer:Lexer):
        self.lexer=lexer
        self.current_token=self.lexer.get_next_token()

    def error(self,err:str):
        raise Exception(err)
            
    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error("Error token type doesn't match")
    
    def factor(self):
        token=self.current_token
        self.eat(INTEGER)
        return token.value


    def expr(self):
        result=self.factor()
        while self.current_token.type in (MULT,PLUS,DIV,MULT):
            op=self.current_token

            if op.type==PLUS:
                self.eat(PLUS)
                result+=self.factor()
            elif op.type==MINUS:
                self.eat(MINUS)
                result-=self.factor()
            elif op.type==MULT:
                self.eat(MULT)
                result=result*self.factor()
            elif op.type==DIV:
                self.eat(DIV)
                result=result/self.factor()
        return result
        # op=self.current_token
        # if op.type==PLUS:
        #     self.eat(PLUS)
        # elif op.type==MINUS:
        #     self.eat(MINUS)

        # right=self.current_token
        # self.eat(INTEGER)

        # if op.type==PLUS:
        #     return left.value+right.value
        # else:
        #     return left.value-right.value
            
def main():
    exp=input("calc>")
    lexer=Lexer(exp)
    inter=Intepreter(lexer)
    result=inter.expr()
    print(result)
if __name__=="__main__":
    main()