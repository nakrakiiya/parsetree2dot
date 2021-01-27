import parser
import symbol
import token
import sys
import getopt

_id = 0


def gen_node_id():
    global _id
    _id = _id + 1
    return 'node' + str(_id)


def to_dot_string(s):
    # TODO convert to dot string without quotes
    return s


def tree2dot(node):
    is_nonterminal = node[0]
    if is_nonterminal:
        result = "{0} [ label = \"{1}\" ];\n".format(node[1], node[2])
        for i in range(3, len(node)):
            child_id = node[i][1]
            result = result + "{0} -- {1};\n".format(node[1], child_id)
        for i in range(3, len(node)):
            result = result + tree2dot(node[i])
    else:
        result = "{0} [ label = \"{1}('{2}')\" ];\n".format(node[1], node[2], to_dot_string(node[3]))
    return result


def convert_tree(node):
    symbol_id = node[0]
    symbol_value = node[1]
    if token.ISNONTERMINAL(symbol_id):
        # non terminal
        result = [True, gen_node_id(), symbol.sym_name[symbol_id]]
        for i in range(1, len(node)):
            result.append(convert_tree(node[i]))
        return result
    else:
        # terminal
        return [False, gen_node_id(), token.tok_name[symbol_id], symbol_value]


def to_dot(infile, outfile):
    print("Parsing {0}...".format(infile))
    source = open(infile).read()
    st = parser.suite(source)
    tree = parser.st2list(st)
    ct = convert_tree(tree)
    converted_str = "graph {\n" + "{0};\n".format(ct[1]) + tree2dot(ct) + "}"
    print("Writing to `{0}'...".format(outfile))
    open(outfile, "w").write(converted_str)


def usage():
    print('''

Convert the parse tree of `file' into Graphviz format.
By default, the output filename is `file.dot'.

Usage:
    python {0} [Options] file...
    
Options:
    -h, --help      Display this message
    
    
    '''.format(sys.argv[0]))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()

    for file in args:
        output_path = file + '.dot'
        to_dot(file, output_path)


if __name__ == "__main__":
    main()


