OP_MUL = "*"
OP_DIV = "%"
OP_ADD = "+"
OP_SUB = "-"
OP_SHR = ">>"
OP_SHL = "<<"
OP_LT = "<"
OP_GT = ">"
OP_EQ = "=="
OP_NEQ = "!="

ASSIGN = "="


SME_FOR_FMT = "for {0} = {1} to {2} {{\n {3} \n}}\n"
SME_IF_FMT = "if ( {0} ) {{\n {1} \n}}\n"
SME_PROC_FMT= "proc {0} ({1}) {{ \n {2} \n }} \n"

SME_BUS_FMT = """
bus {0} {{
{1}
}}
"""

SME_CHANNEL_FMT = "\t{0}: {1};\n"

SME_NETWORK_FMT = """
network {0}() {{
{1}

{2}
}}
"""
