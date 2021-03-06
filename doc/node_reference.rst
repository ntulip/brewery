Node Reference
++++++++++++++

Sources
=======

.. _CSVSourceNode:

CSV Source
----------

.. image:: nodes/csv_file_source_node.png
   :align: right

**Synopsis:** *Read data from a comma separated values (CSV) file.*

**Class:** CSVSourceNode

Source node that reads comma separated file from a filesystem or a remote URL.

It is recommended to configure node fields before running. If you do not do so, fields are
read from the file header if specified by `read_header` flag. Field storage types are set to
`string` and analytical type is set to `typeless`.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - resource
     - File name or URL containing comma separated values
   * - fields
     - fields contained in the file
   * - read_header
     - flag determining whether first line contains header or not
   * - skip_rows
     - number of rows to be skipped
   * - encoding
     - resource data encoding, by default no conversion is performed
   * - delimiter
     - record delimiter character, default is comma ','
   * - quotechar
     - character used for quoting string values, default is double quote

.. _RecordListSourceNode:

Record List Source
------------------

.. image:: nodes/record_list_source_node.png
   :align: right

**Synopsis:** *Provide list of dict objects as data source.*

**Class:** RecordListSourceNode

Source node that feeds records (dictionary objects) from a list (or any other iterable)
object.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - list
     - List of records represented as dictionaries.
   * - fields
     - Fields in the list.

.. _RowListSourceNode:

Row List Source
---------------

.. image:: nodes/row_list_source_node.png
   :align: right

**Synopsis:** *Provide list of lists or tuples as data source.*

**Class:** RowListSourceNode

Source node that feeds rows (list/tuple of values) from a list (or any other iterable)
object.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - list
     - List of rows represented as lists or tuples.
   * - fields
     - Fields in the list.

.. _StreamSourceNode:

Data Stream Source
------------------

.. image:: nodes/row_list_source_node.png
   :align: right

**Synopsis:** *Generic data stream data source node.*

**Class:** StreamSourceNode

Generic data stream source. Wraps a :mod:`brewery.ds` data source and feeds data to the 
output.

The source data stream should configure fields on initialize().

Note that this node is only for programatically created processing streams. Not useable
in visual, web or other stream modelling tools.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - stream
     - Data stream object.

.. _YamlDirectorySourceNode:

YAML Directory Source
---------------------

.. image:: nodes/yaml_directory_source_node.png
   :align: right

**Synopsis:** *Read data from a directory containing YAML files*

**Class:** YamlDirectorySourceNode

Source node that reads data from a directory containing YAML files.

The data source reads files from a directory and treats each file as single record. For example,
following directory will contain 3 records::

    data/
        contract_0.yml
        contract_1.yml
        contract_2.yml

Optionally one can specify a field where file name will be stored.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - path
     - Path to a directory
   * - extension
     - file extension to look for, default is yml. If none is given, then all regular files in the directory are read.
   * - filename_field
     - name of a new field that will contain file name

Record Operations
=================

.. _AggregateNode:

Aggregate Node
--------------

.. image:: nodes/aggregate_node.png
   :align: right

**Synopsis:** *Aggregate values grouping by key fields.*

**Class:** AggregateNode

Aggregate


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - keys
     - List of fields according to which records are grouped
   * - record_count_field
     - Name of a field where record count will be stored. Default is `record_count`

.. _AppendNode:

Append
------

.. image:: nodes/append_node.png
   :align: right

**Synopsis:** *Concatenate input streams.*

**Class:** AppendNode

Sequentialy append input streams. Concatenation order reflects input stream order. The
input streams should have same set of fields.


.. _AuditNode:

Data Audit
----------

.. image:: nodes/data_audit_node.png
   :align: right

**Synopsis:** *Perform basic data audit.*

**Class:** AuditNode

Node chcecks stream for empty strings, not filled values, number distinct values.

Audit note passes following fields to the output:

    * `field_name` - name of a field from input
    * `record_count` - number of records
    * `null_count` - number of records with null value for the field
    * `null_record_ratio` - ratio of null count to number of records
    * `empty_string_count` - number of strings that are empty (for fields of type string)
    * `distinct_count` - number of distinct values (if less than distinct threshold). Set
      to None if there are more distinct values than `distinct_threshold`.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - distinct_threshold
     - number of distinct values to be tested. If there are more than the threshold, then values are not included any more and result `distinct_values` is set to None 

.. _DistinctNode:

Distinct Node
-------------

.. image:: nodes/distinct_node.png
   :align: right

**Synopsis:** *Pass only distinct records (discard duplicates) or pass only duplicates*

**Class:** DistinctNode

Node will pass distinct records with given distinct fields.

If `discard` is ``False`` then first record with distinct keys is passed to the output. This is
used to find all distinct key values.

If `discard` is ``True`` then first record with distinct keys is discarded and all duplicate
records with same key values are passed to the output. This mode is used to find duplicate
records. For example: there should be only one invoice per organisation per month. Set
`distinct_fields` to `organisaion` and `month`, sed `discard` to ``True``. Running this node
should give no records on output if there are no duplicates.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - distinct_fields
     - List of key fields that will be considered when comparing records
   * - discard
     - Field where substition result will be stored. If not set, then original field will be replaced with new value.

.. _MergeNode:

Merge Node
----------

.. image:: nodes/merge_node.png
   :align: right

**Synopsis:** *Merge two or more streams*

**Class:** MergeNode

Merge two or more streams (join).

Inputs are joined in a star-like fashion: one input is considered master and others are 
details adding information to the master. By default master is the first input.
Joins are specified as list of tuples: (`input_tag`, `master_input_key`, `other_input_key`).

Following configuration code shows how to add region and category details:

.. code-block:: python

    node.keys = [ [1, "region_code", "code"], 
                  [2, "category_code", "code"] ]

Master input should have fields `region_code` and `category_code`, other inputs should have
`code` field with respective values equal to master keys.

.. code-block:: python

    node.keys = [ [1, "region_code", "code"], 
                  [2, ("category_code", "year"), ("code", "year")] ]

As a key you might use either name of a sigle field or list of fields for compound keys. If
you use compound key, both keys should have same number of fields. For example, if there is
categorisation based on year:

The detail key might be omitted if it the same as in master input:

.. code-block:: python

    node.keys = [ [1, "region_code"], 
                  [2, "category_code"] ]

Master input should have fields `region_code` and `category_code`, input #1 should have
`region_code` field and input #2 should have `category_code` field.

To filter-out fields you do not want in your output or to rename fields you can use `maps`. It
should be a dictionary where keys are input tags and values are either
:class:`brewery.ds.FieldMap` objects or dictionaries with keys ``rename`` and ``drop``.

Following example renames ``source_region_name`` field in input 0 and drops field `id` in
input 1:

.. code-block:: python

    node.maps = {
                    0: ds.FieldMap(rename = {"source_region_name":"region_name"}),
                    1: ds.FieldMap(drop = ["id"])
                }

It is the same as:

.. code-block:: python

    node.maps = {
                    0: { "rename" = {"source_region_name":"region_name"} },
                    1: { "drop" = ["id"] }
                }

The first option is preferred, the dicitonary based option is provided for convenience
in cases nodes are being constructed from external description (such as JSON dictionary).

.. note::

    Limitations of current implementation (might be improved in the future):

    * only inner join between datasets: that means that only those input records are joined
      that will have matching keys
    * "detail" datasets should have unique keys, otherwise the behaviour is undefined
    * master is considered as the largest dataset

How does it work: all records from detail inputs are read first. Then records from master
input are read and joined with cached input records. It is recommended that the master dataset
set is the largest from all inputs.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - joins
     - Join specification (see node documentation)
   * - master
     - Tag (index) of input dataset which will be considered as master
   * - maps
     - Specification of which fields are passed from input and how they are going to be (re)named
   * - join_types
     - Dictionary where keys are stream tags (indexes) and values are types of join for the stream. Default is 'inner'. -- **Not implemented**

.. _SampleNode:

Sample Node
-----------

.. image:: nodes/sample_node.png
   :align: right

**Synopsis:** *Pass data sample from input to output.*

**Class:** SampleNode

Create a data sample from input stream. There are more sampling possibilities:

* fixed number of records
* % of records, random *(not yet implemented)*
* get each n-th record *(not yet implemented)*

Node can work in two modes: pass sample to the output or discard sample and pass the rest.
The mode is controlled through the `discard` flag. When it is false, then sample is passed
and rest is discarded. When it is true, then sample is discarded and rest is passed.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - sample_size
     - Size of the sample to be passed to the output
   * - discard
     - flag whether the sample is discarded or included

.. _SelectNode:

Select
------

.. image:: nodes/select_node.png
   :align: right

**Synopsis:** *Select records by a predicate function.*

**Class:** SelectNode

Select records that will be selected by a predicate function.


Example: configure a node that will select records where `amount` field is greater than 100

.. code-block:: python

    def select_greater_than(value, threshold):
        return value > threshold

    node.function = select_greater_than
    node.fields = ["amount"]
    node.kwargs = {"threshold": 100}

The `discard` flag controls behaviour of the node: if set to ``True``, then selection is
inversed and fields that function evaluates as ``True`` are discarded. Default is False -
selected records are passed to the output.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - function
     - Predicate function. Should be a callable object.
   * - fields
     - List of field names to be passed to the function.
   * - discard
     - flag whether the selection is discarded or included
   * - kwargs
     - Keyword arguments passed to the predicate function

.. _SetSelectNode:

Set Select
----------

.. image:: nodes/set_select_node.png
   :align: right

**Synopsis:** *Select records by a predicate function.*

**Class:** SetSelectNode

Select records where field value is from predefined set of values.

Use case examples:

* records from certain regions in `region` field
* recprds where `quality` status field is `low` or `medium`


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - field
     - Field to be tested.
   * - value_set
     - set of values that will be used for record selection
   * - discard
     - flag whether the selection is discarded or included

Field Operations
================

.. _BinningNode:

Binning
-------

.. image:: nodes/histogram_node.png
   :align: right

**Synopsis:** *Derive a field based on binned values (histogram)*

**Class:** BinningNode

Derive a bin/category field from a value.

.. warning::

    Not yet implemented

Binning modes:

* fixed width (for example: by 100)
* fixed number of fixed-width bins
* n-tiles by count or by sum
* record rank

    


.. _CoalesceValueToTypeNode:

Coalesce Value To Type Node
---------------------------

.. image:: nodes/coalesce_value_to_type_node.png
   :align: right

**Synopsis:** *Coalesce Value to Type*

**Class:** CoalesceValueToTypeNode

Coalesce values of selected fields, or fields of given type to match the type.

* `string`, `text`
    * Strip strings
    * if non-string, then it is converted to a unicode string
    * Change empty strings to empty (null) values
* `float`, `integer`
    * If value is of string type, perform string cleansing first and then convert them to
      respective numbers or to null on failure


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - fields
     - List of fields to be cleansed. If none given then all fields of known storage type are cleansed
   * - types
     - List of field types to be coalesced (if no fields given)
   * - empty_values
     - dictionary of type -> value pairs to be set when field is considered empty (null) - not yet used

.. _FieldMapNode:

Field Map
---------

.. image:: nodes/field_map_node.png
   :align: right

**Synopsis:** *Rename or drop fields from the stream.*

**Class:** FieldMapNode

Node renames input fields or drops them from the stream.
    


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - map_fields
     - Dictionary of input to output field name.
   * - drop_fields
     - List of fields to be dropped from the stream.

.. _StringStripNode:

String Strip
------------

.. image:: nodes/string_strip_node.png
   :align: right

**Synopsis:** *Strip characters.*

**Class:** StringStripNode

Strip spaces (orother specified characters) from string fields.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - fields
     - List of string fields to be stripped. If none specified, then all fields of storage type `string` are stripped
   * - chars
     - Characters to be stripped. By default all white-space characters are stripped.

.. _TextSubstituteNode:

Text Substitute
---------------

.. image:: nodes/text_substitute_node.png
   :align: right

**Synopsis:** *Substitute text in a field using regular expression.*

**Class:** TextSubstituteNode

Substitute text in a field using regular expression.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - field
     - Field containing a string or text value where substition will be applied
   * - derived_field
     - Field where substition result will be stored. If not set, then original field will be replaced with new value.
   * - substitutions
     - List of substitutions: each substition is a two-element tuple (`pattern`, `replacement`) where `pattern` is a regular expression that will be replaced using `replacement`

.. _ValueThresholdNode:

Value Threshold
---------------

.. image:: nodes/value_threshold_node.png
   :align: right

**Synopsis:** *Bin values based on a threshold.*

**Class:** ValueThresholdNode

Create a field that will refer to a value bin based on threshold(s). Values of `range` type
can be compared against one or two thresholds to get low/high or low/medium/high value bins.

*Note: this node is not yet implemented*

The result is stored in a separate field that will be constructed from source field name and
prefix/suffix.

For example:
    * amount < 100 is low
    * 100 <= amount <= 1000 is medium
    * amount > 1000 is high

Generated field will be `amount_threshold` and will contain one of three possible values:
`low`, `medium`, `hight`

Another possible use case might be for binning after data audit: we want to measure null 
record count and we set thresholds:
    
    * ratio < 5% is ok
    * 5% <= ratio <= 15% is fair
    * ratio > 15% is bad
    
We set thresholds as ``(0.05, 0.15)`` and values to ``("ok", "fair", "bad")``
    


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - thresholds
     - List of fields of `range` type and threshold tuples (field, low, high) or (field, low)
   * - bin_names
     - Names of bins based on threshold. Default is low, medium, high
   * - prefix
     - field prefix to be used, default is none.
   * - suffix
     - field suffix to be used, default is '_bin'

Targets
=======

.. _CSVTargetNode:

CSV Target
----------

.. image:: nodes/csv_target_node.png
   :align: right

**Synopsis:** *Write rows as comma separated values into a file*

**Class:** CSVTargetNode

Node that writes rows into a comma separated values (CSV) file.

:Attributes:
    * resource: target object - might be a filename or file-like object
    * write_headers: write field names as headers into output file
    * truncate: remove data from file before writing, default: True
    


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - resource
     - Target object - file name or IO object.
   * - write_headers
     - Flag determining whether to write field names as file headers.
   * - truncate
     - If set to ``True`` all data from file are removed. Default ``True``

.. _DatabaseTableTargetNode:

Database Table Target
---------------------

.. image:: nodes/sql_table_target.png
   :align: right

**Synopsis:** *Feed data rows into a relational database table*

**Class:** DatabaseTableTargetNode

Feed data rows into a relational database table.
    


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - url
     - Database URL in form: adapter://user:password@host/database
   * - connection
     - SQLAlchemy database connection - either this or url should be specified
   * - table
     - table name
   * - truncate
     - If set to ``True`` all data table are removed prior to node execution. Default is ``False`` - data are appended to the table
   * - create
     - create table if it does not exist or not
   * - replace
     - Set to True if creation should replace existing table or not, otherwise node will fail on attempt to create a table which already exists
   * - buffer_size
     - how many records are collected before they are inserted using multi-insert statement. Default is 1000
   * - options
     - other SQLAlchemy connect() options

.. _FormattedPrinterNode:

Formatted Printer
-----------------

.. image:: nodes/formatted_printer_node.png
   :align: right

**Synopsis:** *Print input using a string formatter to an output IO stream*

**Class:** FormattedPrinterNode

Target node that will print output based on format.

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

    node.header = u"field                            nulls      empty   distinct\n" \
                   "------------------------------------------------------------"
    node.format = u"{field_name:<30.30} {null_record_ratio: >7.2%} "\
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


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - format
     - Format string to be used. Default is to print all field values separated by tab character.
   * - target
     - IO object. If not set then sys.stdout will be used. If it is a string, then it is considered a filename.
   * - delimiter
     - Record delimiter. By default it is new line character.
   * - header
     - Header string - will be printed before printing first record
   * - footer
     - Footer string - will be printed after all records are printed

.. _RecordListTargetNode:

Record List Target
------------------

.. image:: nodes/record_list_target_node.png
   :align: right

**Synopsis:** *Store data as list of dictionaries (records)*

**Class:** RecordListTargetNode

Target node that stores data from input in a list of records (dictionary objects)
object.

To get list of fields, ask for `output_fields`.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - records
     - Created list of records represented as dictionaries.

.. _RowListTargetNode:

Row List Target
---------------

.. image:: nodes/row_list_target_node.png
   :align: right

**Synopsis:** *Store data as list of tuples*

**Class:** RowListTargetNode

Target node that stores data from input in a list of rows (as tuples).

To get list of fields, ask for `output_fields`.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - rows
     - Created list of tuples.

.. _StreamTargetNode:

Data Stream Target
------------------

.. image:: nodes/row_list_target_node.png
   :align: right

**Synopsis:** *Generic data stream data target node.*

**Class:** StreamTargetNode

Generic data stream target. Wraps a :mod:`brewery.ds` data target and feeds data from the 
input to the target stream.

The data target should match stream fields.

Note that this node is only for programatically created processing streams. Not useable
in visual, web or other stream modelling tools.


.. list-table:: Attributes
   :header-rows: 1
   :widths: 40 80

   * - attribute
     - description
   * - stream
     - Data target object.

