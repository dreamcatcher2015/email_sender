/**
 * The first thing to know about are types. The available types in Thrift are:
 *
 *  bool        Boolean, one byte
 *  byte        Signed byte
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 * Did you also notice that Thrift supports C style comments?
 */

namespace py  mailsvc

struct MailObject {
	1:required string       sendto,
	2:string       subject,
	3:string       content,
	4:list<string> attach_files,
	5:i32          priority=1
}

service MailsService{
	i32    send_mails (1:list<MailObject> mails);
	i32    send_mails2 (1:list<string> sendtos, 2:string subject, 3:string content, 4:list<string> attach_files, 5:i32 priority);
}
