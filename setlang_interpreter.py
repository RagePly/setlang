from setlang import setlang,NN,ZZ,RR,RRpos,RRneg,CC,OO,UU,set_range,D_,C_,RR_
import os
import re

# TODO Maybe check for injections
# TODO Tuples inside tuples and similar are not acceptable syntax

def parse_setlang(i_str):
    if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]* *= *\{ *[a-zA-Z_][a-zA-Z0-9_]* *(, *[a-zA-Z_][a-zA-Z0-9_]* *)*:.*\}',i_str):
        i_assignment = i_str.find("=")
        i_lhb = i_str.find("{")
        var_nam = i_str[0:i_assignment].strip()
        expr = i_str[i_lhb+1:-1].strip()
        param, l_def = expr.split(":",maxsplit=1)
        param_vars = {x.strip() for x in param.split(",")}
        if param_vars & _pm.keys():
            print("A parameter can not have the same name as an existing set")
        else:
            _pm.update({var_nam : ()})
            special_characters_after = {' ','~','+','-','&','}',')',']'}
            special_characters_before = {' ','~','+','-','&','{','(','['}
            for var in _pm.keys():
                i = 0
                i = l_def.find(var,i)
                while not i == - 1:
                    if not i == 0:
                        c_before = l_def[i-1]
                        if not c_before in special_characters_before:
                            i = l_def.find(var, i+1)
                            continue

                    if not i + len(var) >= len(l_def):
                        c_after = l_def[i+len(var)]
                        if not c_after in special_characters_after:
                            i = l_def.find(var, i+1)
                            continue 
                    
                    l_def = l_def[:i] + "_pm[\"" + var + "\"][\"set\"]" + l_def[i+len(var):]
                    i = l_def.find(var,i+1)
            parsed_str = "setlang(lambda " + param + ":" + l_def + ")"
            _pm.update({var_nam : {"set":eval(parsed_str), "parsed":parsed_str,"orig":i_str}})
            return True 
    return False


# Global memory
_pm = {}
if __name__ == "__main__":
    with open("content\\greeting.txt","r") as f:
        for l in f.readlines():
            print(l)

    re_1elem = r"((\".+\")|([\-0-9]+\.[0-9]+)|([\-0-9]+))"
    re_tuple = r"(\( *((\".+\")|([\-0-9]+\.[0-9]+)|([\-0-9]+))( *, *((\".+\")|([\-0-9]+\.[0-9]+)|([\-0-9]+)))+ *\))"
    re_list = r"(\[ *((\".+\")|([\-0-9]+\.[0-9]+)|([\-0-9]+))( *, *((\".+\")|([\-0-9]+\.[0-9]+)|([\-0-9]+)))+ *\])"
    re_all = r" *(" + re_1elem + r"|" + re_tuple + r"|" + re_list + r")"

    while True:
        i = input("- ")
        if re.findall(r'print\(.*\)',i):
            print("Invalid Syntax: print(...)")
        elif parse_setlang(i):
            pass
        elif re.fullmatch(re_all + r" +in +[a-zA-Z_][a-zA-Z0-9_]*(\([0-9]+\))?\?",i):
            i_in = len(i) - ("".join(reversed(i))).find(" ni ") - len(" in ")
            elem = i[:i_in]
            set_var = i[i_in + len(" in "):-1]
            if not (setvar := set_var.strip()) in _pm.keys():                
                print("Unknown set: " + setvar)
            else:
                set_var = "_pm[\"" + setvar + "\"][\"set\"]"
                parsed_str = elem + " in " + set_var
                if eval(parsed_str):
                    print("Yes")
                else:
                    print("No")
        elif i == "exit":
            break
        elif i == "sets":
            if _pm:
                for _,v in _pm.items():
                    print(v["orig"])
            else:
                print()
        elif i == "help":
            with open("content\\help.txt") as f:
                for l in f.readlines():
                    print(l)
        elif i == "clear":
            os.system("clear")
        else:
            print("Couldn't parse command")