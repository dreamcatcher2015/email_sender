-- service postgresql start
-- su postgres
-- psql
-- \c mailsdb

-- \h：查看SQL命令的解释，比如\h select。
-- \?：查看psql命令列表。
-- \l：列出所有数据库。-- 
-- \c [database_name]：连接其他数据库。
-- \d：列出当前数据库的所有表格。
-- \d [table_name]：列出某一张表格的结构。
-- \du：列出所有用户。
-- \e：打开文本编辑器。
-- \conninfo：列出当前数据库和连接的信息。

DROP TABLE IF EXISTS mails;
create table mails(
	id serial NOT NULL,
	smtp_host varchar(10) NOT NULL,
	priority integer NOT NULL,
	state integer NOT NULL,
	send_count integer NOT NULL,
	sendto varchar(50) NOT NULL,
	subject text,
	content text,
	attach_files text, 
	create_time   timestamp without time zone,
	loaded_time   timestamp without time zone,
	assigned_time timestamp without time zone,
	sending_time  timestamp without time zone,
	finish_time   timestamp without time zone,
	CONSTRAINT mails_key PRIMARY KEY (id)
); 

DROP TABLE IF EXISTS mails_send_finish;
create table mails_send_finish(
	id serial NOT NULL,
	smtp_host varchar(10) NOT NULL,
	priority integer NOT NULL,
	state integer NOT NULL,
	send_count integer NOT NULL,
	sendto varchar(50) NOT NULL,
	subject text,
	content text,
	attach_files text, 
	create_time   timestamp without time zone,
	loaded_time   timestamp without time zone,
	assigned_time timestamp without time zone,
	sending_time  timestamp without time zone,
	finish_time   timestamp without time zone,
	CONSTRAINT mails_send_finish_key PRIMARY KEY (id)
);

DROP TABLE IF EXISTS mails_send_fail_log;
create table mails_send_fail_log(
	id serial NOT NULL,
	smtp_host varchar(10) NOT NULL,
	priority integer NOT NULL,
	state integer NOT NULL,
	send_count integer NOT NULL,
	sendto varchar(50) NOT NULL,
	subject text,
	content text,
	attach_files text, 
	create_time   timestamp without time zone,
	loaded_time   timestamp without time zone,
	assigned_time timestamp without time zone,
	sending_time  timestamp without time zone,
	finish_time   timestamp without time zone,
	CONSTRAINT mails_send_fail_log_key PRIMARY KEY (id)
);

--创建触发器过程
CREATE OR REPLACE FUNCTION backup_mails_before_delete() RETURNS trigger AS $BODY$ 
	BEGIN
		IF(OLD.state = 5) THEN
			insert into mails_send_finish select OLD.*;
		ELSIF (OLD.state < 0) THEN
			insert into mails_send_fail_log select OLD.*;
		END IF;
		RETURN OLD;
	END;
$BODY$ LANGUAGE 'plpgsql';

--创建触发器
DROP TRIGGER backup_mails_before_delete ON mails;
CREATE TRIGGER backup_mails_before_delete
BEFORE DELETE ON mails FOR EACH ROW 
EXECUTE PROCEDURE backup_mails_before_delete();

