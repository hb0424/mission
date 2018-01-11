gNoversConfig = {
    "websites":{
        "www.pbtxt.com":{
            "hostname": "",
            "webname": "平板电子书网",
            "book_name": "<h1>([\u4e00-\u9fa5]+)</h1>",
            "book_author": "<span class=\"author\">文/(.*?)</span>",
            "book_summary": "<div class=\"intro\" id=\"description.*?<p>(.*?)</p></div>",
            "book_chapter": "<dd><a (.*?)</dd>",
            "book_chapter_name": ">(.*)</a>",
            "book_chapter_url": "href=\"(.*)\">",
            "book_chapter_content": "<div id=\"content.*?</script></div>(.*)<div class=\"con_show_r\">"
        },
        "www.biqudao.com":{
            "hostname": "https://www.biqudao.com",
            "webname": "笔趣岛",
            "book_name": "<h1>([\u4e00-\u9fa5]+)</h1>",
            "book_author": "<p>作.*者：(.*)</p>",
            "book_summary": "<div id=\"intro\">\\r\\n\s*(.*)",
            "book_chapter": "<dd> <a style(.*)</dd>",
            "book_chapter_name": ">(.*)</a>",
            "book_chapter_url": "href=\"(.*)\">",
            "book_chapter_content": "<div id=\"content\">([.\s\S]*)<script>chaptererror"
        },
        "www.biquge.com.tw":{
            "hostname": "http://www.biquge.com.tw",
            "webname": "笔趣阁",
            "book_name": "<h1>([\u4e00-\u9fa5]+)</h1>",
            "book_author": "<p>作.*者：(.*)</p>",
            "book_summary": "<div id=\"intro\">\\r\\n\s*(.*)",
            "book_chapter": "<dd><a (.*?)</dd>",
            "book_chapter_name": ">(.*)</a>",
            "book_chapter_url": "href=\"(.*)\">",
            "book_chapter_content": "<div id=\"content\">([.\s\S]*)<script>read3"
        },
        "www.biqugezw.com":{
            "hostname": "http://www.biqugezw.com",
            "webname": "笔趣阁中文网",
            "book_name": "<h1>([\u4e00-\u9fa5]+)</h1>",
            "book_author": "<p>作.*者：(.*)</p>",
            "book_summary": "<div id=\"intro\">\\r\\n\s*<p>(.*)</p>",
            "book_chapter": "<dd><a (.*)</dd>",
            "book_chapter_name": ">(.*)</a>",
            "book_chapter_url": "href=\"(.*)\">",
            "book_chapter_content": "<div id=\"content\">([.\s\S]*)<script>read3"
        },
        "www.zwdu.com":{
            "hostname": "https://www.zwdu.com",
            "webname": "八一中文网",
            "book_name": "<h1>([\u4e00-\u9fa5]+)</h1>",
            "book_author": "<p>作.*者：(.*)</p>",
            "book_summary": "<div id=\"intro\">[.\s]*?<p>(.*)</p>",
            "book_chapter": "<dd><a (.*?)</dd>",
            "book_chapter_name": ">(.*)</a>",
            "book_chapter_url": "href=\"(.*)\">",
            "book_chapter_content": "<div id=\"content\">([.\s\S]*)<script>read3"
        }

        
    },
    "books":[
        {
            "urls":[
                "http://www.pbtxt.com/103027/"
            ]
        },
        {
            "urls":[
                "https://www.biqudao.com/bqge19874/"
            ]
        },
        {
            "urls":[
                "https://www.zwdu.com/book/15127/"
            ]
        },
        {
            "urls":[
                "http://www.biquge.com.tw/14_14969/"
            ]
        },
        {
            "urls":[
                "http://www.biqugezw.com/23_23496/"
            ]
        },
        {
            "urls":[
                "https://www.biqudao.com/bqge8146/"
            ]
        },
        {
            "urls":[
                "https://www.biqudao.com/bqge110911/"
            ]
        }
    ]
}

