from __future__ import with_statement # support python 2.5

import pandas.core.config as cf
from pandas.core.config import is_int,is_bool,is_text,is_float
from pandas.core.format import detect_console_encoding

"""
This module is imported from the pandas package __init__.py file
in order to ensure that the core.config options registered here will
be available as soon as the user loads the package. if register_option
is invoked inside specific modules, they will not be registered until that
module is imported, which may or may not be a problem.

If you need to make sure options are available even before a certain
module is imported, register them here rather then in the module.

"""


###########################################
# options from the "print_config" namespace

pc_precision_doc="""
: int
    Floating point output precision (number of significant digits). This is
    only a suggestion
"""

pc_colspace_doc="""
: int
    Default space for DataFrame columns, defaults to 12
"""

pc_max_rows_doc="""
: int
"""

pc_max_cols_doc="""
: int
    max_rows and max_columns are used in __repr__() methods to decide if
    to_string() or info() is used to render an object to a string.
    Either one, or both can be set to 0 (experimental). Pandas will figure
    out how big the terminal is and will not display more rows or/and
    columns that can fit on it.
"""

pc_nb_repr_h_doc="""
: boolean
    When True (default), IPython notebook will use html representation for
    pandas objects (if it is available).
"""

pc_date_dayfirst_doc="""
: boolean
    When True, prints and parses dates with the day first, eg 20/01/2005
"""

pc_date_yearfirst_doc="""
: boolean
    When True, prints and parses dates with the year first, eg 2005/01/20
"""

pc_pprint_nest_depth="""
: int
    Defaults to 3.
    Controls the number of nested levels to process when pretty-printing
"""

pc_multi_sparse_doc="""
: boolean
    Default True, "sparsify" MultiIndex display (don't display repeated
    elements in outer levels within groups)
"""

pc_encoding_doc="""
: str/unicode
    Defaults to the detected encoding of the console.
    Specifies the encoding to be used for strings returned by to_string,
    these are generally strings meant to be displayed on the console.
"""

with cf.config_prefix('print_config'):
    cf.register_option('precision', 7, pc_precision_doc, validator=is_int)
    cf.register_option('digits', 7, validator=is_int)
    cf.register_option('float_format', None)
    cf.register_option('column_space', 12, validator=is_int)
    cf.register_option('max_rows', 200, pc_max_rows_doc, validator=is_int)
    cf.register_option('max_colwidth', 50, validator=is_int)
    cf.register_option('max_columns', 0, pc_max_cols_doc, validator=is_int)
    cf.register_option('colheader_justify', 'right',
                       validator=is_text)
    cf.register_option('notebook_repr_html', True, pc_nb_repr_h_doc,
                       validator=is_bool)
    cf.register_option('date_dayfirst', False, pc_date_dayfirst_doc,
                       validator=is_bool)
    cf.register_option('date_yearfirst', False, pc_date_yearfirst_doc,
                       validator=is_bool)
    cf.register_option('pprint_nest_depth', 3, pc_pprint_nest_depth,
                       validator=is_int)
    cf.register_option('multi_sparse', True, pc_multi_sparse_doc,
                       validator=is_bool)
    cf.register_option('encoding', detect_console_encoding(), pc_encoding_doc,
                    validator=is_text)
