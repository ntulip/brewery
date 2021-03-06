# -*- coding: utf-8 -*-

import base
import brewery.ds as ds
import sys

class StreamTargetNode(base.TargetNode):
    """Generic data stream target. Wraps a :mod:`brewery.ds` data target and feeds data from the 
    input to the target stream.

    The data target should match stream fields.

    Note that this node is only for programatically created processing streams. Not useable
    in visual, web or other stream modelling tools.
    """
    
    __node_info__ = {
        "label" : "Data Stream Target",
        "icon": "row_list_target_node",
        "description" : "Generic data stream data target node.",
        "attributes" : [
            {
                 "name": "stream",
                 "description": "Data target object."
            }
        ]
    }
    def __init__(self, stream):
        super(StreamTargetNode, self).__init__()
        self.stream = stream

    def initialize(self):
        # if self.stream_type not in data_sources:
        #     raise ValueError("No data source of type '%s'" % stream_type)
        # stream_info = data_sources[self.stream_type]
        # if "class" not in stream_info:
        #     raise ValueError("No stream class specified for data source of type '%s'" % stream_type)

        # self.stream = stream_class(**kwargs)
        # self.stream.fields = 
        self.stream.initialize()
            
    def run(self):
        for row in self.input.rows():
            stream.append(row)
        
    def finalize(self):
        self.stream.finalize()

class RowListTargetNode(base.TargetNode):
    """Target node that stores data from input in a list of rows (as tuples).
    
    To get list of fields, ask for `output_fields`.
    """

    __node_info__ = {
        "label" : "Row List Target",
        "description" : "Store data as list of tuples",
        "attributes" : [
            {
                 "name": "rows",
                 "description": "Created list of tuples."
            }
        ]
    }

    def __init__(self, a_list = None):
        super(RowListTargetNode, self).__init__()
        if a_list:
            self.list = a_list
        else:
            self.list = []

    def run(self):
        self.list = []
        for row in self.input.rows():
            self.list.append(row)
    @property
    def rows(self):
        return self.list        
        
class RecordListTargetNode(base.TargetNode):
    """Target node that stores data from input in a list of records (dictionary objects)
    object.
    
    To get list of fields, ask for `output_fields`.
    
    """

    __node_info__ = {
        "label" : "Record List Target",
        "description" : "Store data as list of dictionaries (records)",
        "attributes" : [
            {
                 "name": "records",
                 "description": "Created list of records represented as dictionaries."
            }
        ]
    }
    def __init__(self, a_list = None):
        super(RecordListTargetNode, self).__init__()
        if a_list:
            self.list = a_list
        else:
            self.list = []

    def run(self):
        self.list = []
        for record in self.input.records():
            self.list.append(record)

    @property
    def records(self):
        return self.list

class CSVTargetNode(base.TargetNode):
    """Node that writes rows into a comma separated values (CSV) file.
    
    :Attributes:
        * resource: target object - might be a filename or file-like object
        * write_headers: write field names as headers into output file
        * truncate: remove data from file before writing, default: True
        
    """
    __node_info__ = {
        "label" : "CSV Target",
        "description" : "Write rows as comma separated values into a file",
        "attributes" : [
            {
                 "name": "resource",
                 "description": "Target object - file name or IO object."
            },
            {
                 "name": "write_headers",
                 "description": "Flag determining whether to write field names as file headers."
            },
            {
                 "name": "truncate",
                 "description": "If set to ``True`` all data from file are removed. Default ``True``"
            }
        ]
    }
    
    def __init__(self, *args, **kwargs):
        super(CSVTargetNode, self).__init__()
        self.kwargs = kwargs
        self.args = args
        self.stream = None

    def initialize(self):
        self.stream = ds.CSVDataTarget(*self.args, **self.kwargs)

        self.stream.fields = self.input_fields
        self.stream.initialize()

    def run(self):
        for row in self.input.rows():
            self.stream.append(row)

    def finalize(self):
        self.stream.finalize()


class FormattedPrinterNode(base.TargetNode):
    """Target node that will print output based on format.

    Refer to the python formatting guide:
    
        http://docs.python.org/library/string.html

    Example:
    
    Consider we have a data with information about donations. We want to pretty print two fields:
    `project` and `requested_amount` in the form::
    
        Hlavicka - makovicka                                            27550.0
        Obecna kniznica - symbol moderneho vzdelavania                 132000.0
        Vzdelavanie na europskej urovni                                 60000.0
    
    Node for given format is created by:
    
    .. code-block:: python
    
        node = FormattedPrinterNode(format = u"{project:<50.50} {requested_amount:>20}")

    Following format can be used to print output from an audit node:

    .. code-block:: python

        node.header = u"field                            nulls      empty   distinct\\n" \\
                       "------------------------------------------------------------"
        node.format = u"{field_name:<30.30} {null_record_ratio: >7.2%} "\\
                       "{empty_string_count:>10} {distinct_count:>10}"

    Output will look similar to this::

        field                            nulls      empty   distinct
        ------------------------------------------------------------
        file                             0.00%          0         32
        source_code                      0.00%          0          2
        id                               9.96%          0        907
        receiver_name                    9.10%          0       1950
        project                          0.05%          0       3628
        requested_amount                22.90%          0        924
        received_amount                  4.98%          0        728
        source_comment                  99.98%          0          2

    """

    __node_info__ = {
        "label" : "Formatted Printer",
        "icong": "formatted_printer_node",
        "description" : "Print input using a string formatter to an output IO stream",
        "attributes" : [
            {
                 "name": "format",
                 "description": "Format string to be used. Default is to print all field values "
                                "separated by tab character."
            },
            {
                 "name": "target",
                 "description": "IO object. If not set then sys.stdout will be used. "
                                "If it is a string, then it is considered a filename."
            },
            {
                 "name": "delimiter",
                 "description": "Record delimiter. By default it is new line character."
            },
            {
                 "name": "header",
                 "description": "Header string - will be printed before printing first record"
            },
            {
                 "name": "footer",
                 "description": "Footer string - will be printed after all records are printed"
            }
        ]
    }
    def __init__(self, format = None, target = sys.stdout, delimiter = None, header = None,
                 footer = None):
        super(FormattedPrinterNode, self).__init__()
        self.format = format
        
        self.target = target
        self.header = header
        self.footer = footer

        if delimiter:
            self.delimiter = delimiter
        else:
            self.delimiter = '\n'
            
        self.handle = None
        self.close_handle = False

    def run(self):
        if type(self.target) == str or type(self.target) == unicode:
            self.handle = open(self.target, "w")
            self.close_handle = True
        else:
            self.handle = self.target
            self.close_handle = False
        
        names = self.input_fields.names()

        if self.format:
            format_string = self.format
        else:
            fields = []
            for name in names:
                fields.append(u"{" + name + u"}")
                
            format_string = u"" + u"\t".join(fields)

        if self.header:
            self.handle.write(self.header)
            if self.delimiter:
                self.handle.write(self.delimiter)
            
        for record in self.input.records():
            self.handle.write(format_string.format(**record).encode("utf-8"))
            
            if self.delimiter:
                self.handle.write(self.delimiter)

        if self.footer:
            self.handle.write(self.footer)
            if self.delimiter:
                self.handle.write(self.delimiter)

        self.handle.flush()
        
    def finalize(self):
        if self.handle:
            self.handle.flush()
            if self.close_handle:
                self.handle.close()

class DatabaseTableTargetNode(base.TargetNode):
    """Feed data rows into a relational database table.
    """
    __node_info__ = {
        "label": "Database Table Target",
        "icon": "sql_table_target",
        "description" : "Feed data rows into a relational database table",
        "attributes" : [
            {
                 "name": "url",
                 "description": "Database URL in form: adapter://user:password@host/database"
            },
            {
                 "name": "connection",
                 "description": "SQLAlchemy database connection - either this or url should be specified",
            },
            {
                 "name": "table",
                 "description": "table name"
            },
            {
                 "name": "truncate",
                 "description": "If set to ``True`` all data table are removed prior to node "
                                "execution. Default is ``False`` - data are appended to the table"
            },
            {
                 "name": "create",
                 "description": "create table if it does not exist or not"
            },
            {
                 "name": "replace",
                 "description": "Set to True if creation should replace existing table or not, "
                                "otherwise node will fail on attempt to create a table which "
                                "already exists"
            },
            {
                "name": "buffer_size",
                "description": "how many records are collected before they are "
                              "inserted using multi-insert statement. "
                              "Default is 1000"
            },
            {
                 "name": "options",
                 "description": "other SQLAlchemy connect() options"
            }
        ]
    }

    def __init__(self, *args, **kwargs):
        super(DatabaseTableTargetNode, self).__init__()
        self.kwargs = kwargs
        self.args = args
        self.stream = None

    def initialize(self):
        self.stream = ds.SQLDataTarget(*self.args, **self.kwargs)

        self.stream.fields = self.input_fields
        self.stream.initialize()

    def run(self):
        for row in self.input.rows():
            self.stream.append(row)

    def finalize(self):
        self.stream.finalize()
