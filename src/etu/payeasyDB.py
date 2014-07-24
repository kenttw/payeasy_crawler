import sqlite3
from etu.payEasyClass import prodcut

def savePostToSqlite(plist, cid):
    try:
        conn = sqlite3.connect('../payeasy_'+ str(cid) +'.sqlite')
        c = conn.cursor()
        
        # Create table
        table_name = "payeasy"
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
        count  = c.fetchone()
        if(count[0]==0):
            c.execute('CREATE TABLE '+ table_name +' (p_pid text ,p_url text , p_img text , p_description text , p_price text )')
            conn.commit()
            
            
        
        # Insert a row of data
        for p in plist:
            
#             pro = prodcut()
            pro = p
#             p_url = p[0]
#             p_img = p[1]
#             p_description = p[2]
#             p_price = p[3]
#             c.execute('INSERT INTO ' + table_name  + ' VALUES (?,?,?,?,?)', [p_url,p_img,p_description,p_price])
            c.execute('INSERT INTO ' + table_name  + ' VALUES (?,?,?,?,?)', [pro.p_pid,pro.p_url,pro.p_img,pro.p_description,pro.p_price])

#             print("add:",post)        
        # Save (commit) the changes
        conn.commit()
        
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    except (RuntimeError, ), e:
        raise