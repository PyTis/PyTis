#!/usr/bin/env ruby
# This script currently does not work!
# This is a simple approach to track database schema changes in PostgreSQL.
# In some way it is similar to diff program, finding out structure changes
# and results in  SQL script to upgrade to new schema.
# 
# Differences are tracked on schemas, domains, sequences, views, tables, indices, constraints, rules, functions, triggers.
# Two objects with the same name are considered equal if they have the same definitions. 
#
# Missing features: tracking of ownership,  user rights, object dependencies, table inheritance, type casts, aggregates, operators.
# 
# Usage:
#    ./pg_diff dbname=db_v03_dev dbname=db_v04_dev
# 
# Developed using PostgreSQL v8.0.3, v8.1 with ruby-postgres libpq binding (20051127 snapshot).
# 

require 'postgres'
module PostgreSqlSchema

class Attribute
  attr_accessor :name, :type_def, :notnull, :default
  def initialize(name, typedef, notnull, default)
    @name = name
    @type_def = typedef
    @notnull = notnull
    @default = default
  end
  def definition
    out = ['    ', @name,  @type_def]
    out << 'NOT NULL' if @notnull
    out << 'DEFAULT ' + @default if @default
    out.join(" ")
  end
  def == (other)
    definition == other.definition
  end
end

class Table
  attr_accessor :table_name, :schema, :attributes, :constraints, :indexes
  
  def initialize(conn, schema, table_name)
    @schema = schema
    @table_name = table_name
    @attributes = {}
    @constraints = {}
    @indexes = {}
    @atlist = []
    
    att_query = <<-EOT
      select attname, format_type(atttypid, atttypmod) as a_type, attnotnull,  pg_get_expr(adbin, attrelid) as a_default 
      from pg_attribute left join pg_attrdef  on (adrelid = attrelid and adnum = attnum) 
      where attrelid = '#{schema}.#{table_name}'::regclass and not attisdropped and attnum > 0 
      order by attnum
    EOT
    conn.query(att_query).each do |row|
      attname = row[0]
      @attributes[attname] = Attribute.new(attname, row[1], row[2], row[3])
      @atlist << attname
    end
  
    ind_query = <<-EOT
      select indexrelid::regclass as indname, pg_get_indexdef(indexrelid) as def 
      from pg_index where indrelid = '#{schema}.#{table_name}'::regclass and not indisprimary
    EOT
    conn.query(ind_query).each do |row|
      @indexes[row[0]] = row[1]
    end

    cons_query = <<-EOT
      select conname, pg_get_constraintdef(oid) from pg_constraint where conrelid = '#{schema}.#{table_name}'::regclass
    EOT
    conn.query(cons_query).each do |row|
      @constraints[row[0]] = row[1]
    end
    @constraints.keys.each do |cname|
      @indexes.delete("#{schema}.#{cname}") if has_index?(cname)
    end
  end
  
  def has_attribute?(name)
    @attributes.has_key?(name)
  end

  def has_index?(name)
    @indexes.has_key?(name) || @indexes.has_key?("#{schema}.#{name}")
  end
  
  def has_constraint?(name)
    @constraints.has_key?(name)
  end
  
  def table_creation
    out = ["CREATE TABLE #{name} ("]
    stmt = []
    @atlist.each do |attname|
      stmt << @attributes[attname].definition
    end
    out << stmt.join(",\n")
    out << ");"
    out.join("\n")
  end

  def name
    "#{schema}.#{table_name}"
  end
  
  def constr_creation
    out = []
    @constraints.each do |n, c|
      out << "ALTER TABLE #{name} ADD CONSTRAINT #{n} #{c};" 
    end
    out.join("\n")
  end
  
  def index_creation
    out = []
    @indexes.values.each do |c|
      out << (c+";")
    end
    out.join("\n")
  end
end

class Sequence

  def initialize(conn, sch, relname)
     @name = "#{sch}.#{relname}"
  end
  
  def definition
    "CREATE SEQUENCE #{@name} ;"
  end
end

class View
  attr_reader :def, :name 
  
  def initialize(conn, sch, relname)
    @name = "#{sch}.#{relname}"
    view_qery = <<-EOT
      SELECT pg_catalog.pg_get_viewdef('#{@name}'::regclass, true)
    EOT
    @def = conn.query(view_qery)[0][0]
  end
  
  def definition
    "CREATE VIEW #{@name} AS #{@def}"
  end
end

class Database
  attr_accessor :tables, :views, :sequences, :schemas, :domains, :rules, :functions, :triggers
  def initialize(conn)
     cls_query = <<-EOT
      SELECT n.nspname, c.relname, c.relkind
      FROM pg_catalog.pg_class c
      LEFT JOIN pg_catalog.pg_user u ON u.usesysid = c.relowner
      LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
      WHERE c.relkind IN ('r','S','v')
      AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
      ORDER BY 1,2;
    EOT
    @views = {}
    @tables = {}
    @sequences = {}
    @schemas = {}
    @domains = {}
    @functions = {}
    @rules = {}
    @triggers = {}
    
    conn.query(cls_query).each do |row|
      schema, relname, relkind = row
      case relkind
        when 'r' then @tables["#{schema}.#{relname}"] = Table.new(conn, schema, relname)
        when 'v' then @views ["#{schema}.#{relname}"] = View.new(conn, schema, relname)
        when 'S' then @sequences["#{schema}.#{relname}"] = Sequence.new(conn, schema, relname)
      end
    end
    
  domain_qry = <<-EOT
    SELECT n.nspname, t.typname,  pg_catalog.format_type(t.typbasetype, t.typtypmod) || ' ' ||
       CASE WHEN t.typnotnull AND t.typdefault IS NOT NULL THEN 'not null default '||t.typdefault
            WHEN t.typnotnull AND t.typdefault IS NULL THEN 'not null'
            WHEN NOT t.typnotnull AND t.typdefault IS NOT NULL THEN 'default '||t.typdefault
            ELSE ''
       END 
    FROM pg_catalog.pg_type t
       LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
    WHERE t.typtype = 'd'
    ORDER BY 1, 2
  EOT
    conn.query(domain_qry).each do |row|
      @domains["#{row[0]}.#{row[1]}"] = row[2]
    end

    schema_qry = <<-EOT
      select nspname from pg_namespace
    EOT
    conn.query(schema_qry).each do |row|
      @schemas[row[0]]=row[0]
    end

    func_query = <<-EOT
     SELECT proname AS function_name
     , nspname AS namespace
     , lanname AS language_name
     , pg_catalog.obj_description(pg_proc.oid, 'pg_proc') AS comment
     , proargtypes AS function_args
     , proargnames AS function_arg_names
     , prosrc AS source_code
     , proretset AS returns_set
     , prorettype AS return_type,
     provolatile, proisstrict, prosecdef
     FROM pg_catalog.pg_proc
     JOIN pg_catalog.pg_language ON (pg_language.oid = prolang)
     JOIN pg_catalog.pg_namespace ON (pronamespace = pg_namespace.oid)
     JOIN pg_catalog.pg_type ON (prorettype = pg_type.oid)
     WHERE pg_namespace.nspname !~ 'pg_catalog|information_schema'
     AND proname != 'plpgsql_call_handler'
     AND proname != 'plpgsql_validator'
    EOT
    conn.exec(func_query).result.each do |tuple|
      func = Function.new(conn, tuple)
      @functions[func.signature] = func 
    end

    rule_query = <<-EOT
    select  schemaname || '.' ||  tablename || '.' || rulename as rule_name, 
            schemaname || '.' ||  tablename as tab_name,
      rulename, definition
    from pg_rules
    where schemaname !~ 'pg_catalog|information_schema'
    EOT
    conn.exec(rule_query).result.each do |tuple|
      @rules[tuple['rule_name']] = Rule.new(tuple['tab_name'], tuple['rulename'], tuple['definition'])
    end

    trigger_query =  <<-EOT
    select nspname || '.' || relname as tgtable, tgname, pg_get_triggerdef(t.oid) as tg_def
    from pg_trigger t join pg_class c ON (tgrelid = c.oid ) JOIN pg_namespace n ON (c.relnamespace = n.oid)
    where not tgisconstraint
    and nspname !~ 'pg_catalog|information_schema'
    EOT
    conn.exec(trigger_query).result.each do |tuple|
      @triggers[tuple['tgtable'] + "." + tuple['tgname']] = Trigger.new(tuple['tgtable'], tuple['tgname'], tuple['tg_def'])
    end
  end
end

class Rule
  attr_reader :table_name, :name, :definition
  def initialize(table_name, name, df)
    @table_name = table_name
    @name = name
    @definition = df
  end
  def == (other)
    other.definition == definition
  end
end

class Trigger
  attr_reader :table_name, :name, :definition
  def initialize(table_name, name, df)
    @table_name = table_name
    @name = name
    @definition = df + ";"
  end
  def == (other)
    other.definition == definition
  end
end

class Function
  def initialize(conn, tuple)
    @name = tuple['namespace'] + "." + tuple['function_name']
    @language = tuple['language_name']
    @src = tuple['source_code']
    @returns_set = tuple['returns_set']
    @return_type = format_type(conn, tuple['return_type'])
    @tipes = tuple['function_args'].split(" ")
    if tuple['function_arg_names'] && tuple['function_arg_names'] =~ /^\{(.*)\}$/
      @arnames = $1.split(',')
    elsif tuple['function_arg_names'].is_a? Array # my version of ruby-postgres
      @arnames = tuple['function_arg_names']
    else
      @arnames = [""] * @tipes.length
    end
    alist = []
    @tipes.each_with_index do |typ,idx|
      alist << (@arnames[idx] +" " + format_type(conn, typ))
    end
    @arglist = alist.join(" , ")
    @strict = tuple['proisstrict'] ? ' STRICT' : ''
    @secdef = tuple['prosecdef'] ? ' SECURITY DEFINER' : ''
    @volatile = case tuple['provolatile']
      when 'i' then ' IMMUTABLE'
      when 's' then ' STABLE'
      else ''
    end
  end
  def signature
    "#{@name}(#{@arglist})"
  end
  def definition
    <<-EOT
CREATE OR REPLACE FUNCTION #{@name} (#{@arglist}) RETURNS #{@returns_set ? 'SETOF' : ''} #{@return_type} AS $_$#{@src}$_$ LANGUAGE '#{@language}' #{@volatile}#{@strict}#{@secdef};
EOT
  end
  def == (other)
    definition == other.definition
  end
  def format_type(conn, oid)
    t_query = <<-EOT
    SELECT pg_catalog.format_type(pg_type.oid, typtypmod) AS type_name
     FROM pg_catalog.pg_type
     JOIN pg_catalog.pg_namespace ON (pg_namespace.oid = typnamespace)
     WHERE pg_type.oid = 
    EOT
    return conn.query(t_query + oid.to_s)[0][0]
  end
end
class Diff
 
  def initialize(old_db_spec, new_db_spec)
    @old_conn = PGconn.new(old_db_spec)
    @new_conn = PGconn.new(new_db_spec)
    @sections = [
      :triggers_drop,
      :rules_drop,
      :functions_drop,
      :indices_drop ,
      :constraints_drop,
      :views_drop,
      :sequences_drop ,
      :tables_drop ,
      :domains_drop ,
      :schemas_drop , 
      :schemas_create,
      :domains_create,
      :sequences_create,
      :tables_create ,
      :table_changes ,
      :views_create ,
      :functions_create ,
      :rules_create ,
      :triggers_create ,
      :indices_create,
      :constraints_create
    ]
    @script = {}
    @sections.each {|s| @script[s] = []}
  end
  
  def run_compare
    @old_database = Database.new(@old_conn)
    @new_database = Database.new(@new_conn)
    compare_schemas
    compare_domains
    compare_sequences
    compare_triggers_drop
    compare_rules_drop
    compare_views_drop
    compare_table_attrs
    compare_views_create
    compare_functions
    compare_rules_create
    compare_triggers_create
    compare_table_constraints
  end

  def add_script(section, statement)
    @script[section] << statement
  end
  
  def compare_schemas
    @old_database.schemas.keys.each do |name|
      add_script(:schemas_drop ,  "DROP SCHEMA #{name};") unless @new_database.schemas.has_key?(name)
    end
    @new_database.schemas.keys.each do |name|
      add_script(:schemas_create ,  "CREATE SCHEMA #{name};") unless @old_database.schemas.has_key?(name)
    end
  end

  def compare_domains
    @old_database.domains.keys.each do |name|
      add_script(:domains_drop ,  "DROP DOMAIN #{name} CASCADE;") unless @new_database.domains.has_key?(name)
    end
    @new_database.domains.each do |name, df|
      add_script(:domains_create ,  "CREATE DOMAIN #{name} AS #{df};") unless @old_database.domains.has_key?(name)
      old_domain = @old_database.domains[name]
      if old_domain && old_domain != df
         add_script(:domains_drop, "DROP DOMAIN #{name} CASCADE;")
         add_script(:domains_create,  "-- [changed domain] :")
         add_script(:domains_create,  "-- OLD: #{old_domain}")
         add_script(:domains_create,  "CREATE DOMAIN #{name} AS #{df};") 
      end
    end
  end

  def compare_sequences
    @old_database.sequences.keys.each do |name|
      add_script(:sequences_drop ,  "DROP SEQUENCE #{name} CASCADE;") unless @new_database.sequences.has_key?(name)
    end
    @new_database.sequences.keys.each do |name|
      add_script(:sequences_create ,  "CREATE SEQUENCE #{name};") unless @old_database.sequences.has_key?(name)
    end
  end
  
  def compare_functions
    @old_database.functions.keys.each do |name|
      add_script(:functions_drop ,  "DROP FUNCTION #{name} CASCADE;") unless @new_database.functions.has_key?(name)
    end
    @new_database.functions.each do |name, func|
      add_script(:functions_create ,   func.definition) unless @old_database.functions.has_key?(name)
      old_function = @old_database.functions[name]
      if old_function && old_function.definition != func.definition
        add_script(:functions_create , '-- [changed function] :')
        add_script(:functions_create , '-- OLD :')
        add_script(:functions_create ,  old_function.definition.gsub(/^/, "-->  ") )
        add_script(:functions_create ,   func.definition) 
      end
    end
  end

  def compare_rules_drop
    @old_database.rules.each do |name, rule|
      add_script(:rules_drop ,  "DROP RULE #{rule.name} ON #{rule.table_name} CASCADE;") unless @new_database.rules.has_key?(name)
    end
  end
  
  def compare_rules_create
    @new_database.rules.each do |name, rule|
      add_script(:rules_create ,   rule.definition) unless @old_database.rules.has_key?(name)
      old_rule = @old_database.rules[name]
      if old_rule && old_rule != rule
        add_script(:rules_drop ,  "DROP RULE #{rule.name} ON #{rule.table_name} CASCADE;") 
        add_script(:rules_create ,  "-- [changed rule] :")
        add_script(:rules_create ,  "-- OLD: #{old_rule.definition}")
        add_script(:rules_create ,   rule.definition )
      end
    end
  end

  def compare_triggers_drop
    @old_database.triggers.each do |name, trigger|
      add_script(:triggers_drop ,  "DROP trigger #{trigger.name} ON #{trigger.table_name} CASCADE;") unless @new_database.triggers.has_key?(name)
    end
  end
  
  def compare_triggers_create
    @new_database.triggers.each do |name, trigger|
      add_script(:triggers_create ,   trigger.definition) unless @old_database.triggers.has_key?(name)
      old_trigger = @old_database.triggers[name]
      if old_trigger && old_trigger != trigger
        add_script(:triggers_drop ,  "DROP trigger #{trigger.name} ON #{trigger.table_name} CASCADE;") 
        add_script(:triggers_create ,  "-- [changed trigger] :")
        add_script(:triggers_create ,  "-- OLD #{old_trigger.definition}")
        add_script(:triggers_create ,   trigger.definition) 
      end
    end
  end

  def compare_views_drop
    @old_database.views.keys.each do |name|
      add_script(:views_drop ,  "DROP VIEW #{name};") unless @new_database.views.has_key?(name)
    end
  end

  def compare_views_create
    @new_database.views.each do |name, df|
      add_script(:views_create ,   df.definition) unless @old_database.views.has_key?(name)
      old_view = @old_database.views[name]
      if old_view && df.definition != old_view.definition
        add_script(:views_drop ,  "DROP VIEW #{name};")
        add_script(:views_create ,  "-- [changed view] :")
        add_script(:views_create ,  "-- #{old_view.definition.gsub(/\n/, ' ')}")
        add_script(:views_create ,  df.definition)
      end
    end
  end
  
  def compare_table_attrs
    @old_database.tables.each do |name, table|
      add_script(:tables_drop, "DROP TABLE #{name} CASCADE;") unless @new_database.tables.has_key?(name)
    end
    @to_compare = []
    @new_database.tables.each do |name, table|
      unless @old_database.tables.has_key?(name)
        add_script(:tables_create ,  table.table_creation)
        add_script(:indices_create ,  table.index_creation) unless table.indexes.empty?
        @to_compare << name
      else
        diff_attributes(@old_database.tables[name], table)
        diff_indexes(@old_database.tables[name], table)
        @to_compare << name
      end
    end
  end

  def compare_table_constraints
    @c_check = []
    @c_primary = []
    @c_unique = []
    @c_foreign = []
    @to_compare.each do |name|
      if @old_database.tables[name] 
        diff_constraints(@old_database.tables[name], @new_database.tables[name])
      else
        @new_database.tables[name].constraints.each do |cname, cdef|
          add_cnstr(name,  cname, cdef) 
        end
      end
    end
    @script[:constraints_create] += @c_check
    @script[:constraints_create] += @c_primary
    @script[:constraints_create] += @c_unique
    @script[:constraints_create] += @c_foreign
  end

  def output
    out = []
    @sections.each do |sect|
      if @script[sect].empty?
         out << "-- [SKIP SECTION : #{sect.to_s.upcase}] : no changes\n"
      else
         out << "-- [START SECTION : #{sect.to_s.upcase}]"
         out += @script[sect]
         out << "-- [END SECTION : #{sect.to_s.upcase}]\n"
      end
    end
    out.join("\n")
  end
  
  def diff_attributes(old_table, new_table)
    dropped = []
    added   = []
    changed = []
    old_table.attributes.keys.each do |attname| 
      if new_table.has_attribute?(attname)
        changed << attname if old_table.attributes[attname] != new_table.attributes[attname]
      else
        dropped << attname
      end
    end
    new_table.attributes.keys.each do |attname|
      added << attname unless old_table.has_attribute?(attname)
    end
    add_script(:table_changes ,  "--  [#{old_table.name}] dropped attributes") unless dropped.empty?
    dropped.each do |attname|
      add_script(:table_changes ,  "ALTER TABLE #{old_table.name} DROP COLUMN #{attname} CASCADE;")
    end
    add_script(:table_changes ,  "--  [#{old_table.name}] added attributes") unless added.empty?
    added.each do |attname|
      add_script(:table_changes ,  "ALTER TABLE #{old_table.name} ADD COLUMN #{new_table.attributes[attname].definition};")
    end
    add_script(:table_changes ,  "--  [#{old_table.name}] changed attributes") unless changed.empty?
    changed.each do |attname|
      old_att = old_table.attributes[attname]
      new_att = new_table.attributes[attname]
      add_script(:table_changes ,  "-- attribute: #{attname}")
      add_script(:table_changes ,  "-- OLD : #{old_att.definition}")
      add_script(:table_changes ,  "-- NEW : #{new_att.definition}")
      if old_att.type_def != new_att.type_def
        add_script(:table_changes ,  "ALTER TABLE #{old_table.name} ALTER COLUMN #{attname} TYPE #{new_att.type_def};")
      end
      if old_att.default != new_att.default
        if new_att.default.nil?
          add_script(:table_changes ,  "ALTER TABLE #{old_table.name} ALTER COLUMN #{attname} DROP DEFAULT;")
        else
          add_script(:table_changes ,  "ALTER TABLE #{old_table.name} ALTER COLUMN #{attname} SET DEFAULT #{new_att.default};")
        end
      end
      if old_att.notnull != new_att.notnull
        add_script(:table_changes ,  "ALTER TABLE #{old_table.name} ALTER COLUMN #{attname} #{new_att.notnull ? 'SET' : 'DROP'} NOT NULL;")
      end
    end
  end

  def diff_constraints(old_table, new_table)
    dropped = []
    added   = []
    
    old_table.constraints.keys.each do |conname| 
      if new_table.has_constraint?(conname)
        if old_table.constraints[conname] != new_table.constraints[conname]
          dropped << conname
          added << conname
        end
      else
        dropped << conname
      end
    end
    new_table.constraints.keys.each do |conname| 
      added << conname unless old_table.has_constraint?(conname)
    end

    dropped.each do |name|  
      add_script(:constraints_drop ,  "ALTER TABLE #{old_table.name} DROP CONSTRAINT #{name};")
    end
    
    added.each do |name|  
      add_cnstr(old_table.name,  name, new_table.constraints[name]) 
    end
  end

  def add_cnstr(tablename, cnstrname, cnstrdef)
    c_string = "ALTER TABLE #{tablename} ADD CONSTRAINT #{cnstrname} #{cnstrdef} ;"
    case cnstrdef
      when /^CHECK /   then @c_check  << c_string
      when /^PRIMARY / then @c_primary << c_string
      when /^FOREIGN / then @c_foreign << c_string
      when /^UNIQUE /  then @c_unique  << c_string
    end
  end
  
  def diff_indexes(old_table, new_table)
    dropped = []
    added   = []
    
    old_table.indexes.keys.each do |name| 
      if new_table.has_index?(name)
        if old_table.indexes[name] != new_table.indexes[name]
          dropped << name
          added << name
        end
      else
        dropped << name
      end
    end
    new_table.indexes.each do |name| 
      added << name unless old_table.has_index?(name)
    end
   
    dropped.each do |name|  
      add_script(:indices_drop ,  "DROP INDEX #{name};")
    end
    added.each do |name|
      add_script(:indices_create ,  (new_table.indexes[name] + ";")) if new_table.indexes[name]
    end
  end

end

end

def parse_conn_params(str)
  h = {}
  str.split(/:/).each{|pair| key, value = pair.split('=', 2); h[key]=value}
  h
end

  diff = PostgreSqlSchema::Diff.new(parse_conn_params(ARGV[0]), parse_conn_params(ARGV[1]) )
  diff.run_compare
  puts diff.output


