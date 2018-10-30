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


SME_VARDECL_FMT = "var {0}: {1}{2} = {3};\n"
SME_FOR_FMT = "for {0} = {1} to {2} {{\n{3}\n}}\n"
SME_IF_FMT = "if ( {0} ) {1}"
SME_PROC_FMT= "proc {0} ({1})\n{2} {{\n{3}\n}} \n"
SME_BUS_FMT = """
{0} bus {1} {{
{2}}};
"""
SME_BUS_MODIFIER_EXPOSED="exposed"
SME_BUS_MODIFIER_NONE=""
SME_CHANNEL_FMT = "{0}: {1};\n"

SME_NETWORK_FMT = """
network {0}() {{
{1}
{2}
}}
"""

