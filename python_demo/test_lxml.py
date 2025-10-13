from lxml import etree

html='''
<html>
<body>
    <div>
        div中的文本
        <p class='firstp' role='listitem' data-asin='B0ASDFK'>段落文本<span>嵌套的文本</span></p>
        <p role='listitem' data-asin='B0EEEFDS'>第二段</p>
        <p class='secondp' data-asin='B0EEffds'>第三段</p>
        
    </div>
</body>
</html>
'''
root = etree.HTML(html)
# print(root.tag)
print(root.xpath('//p/text()'))  #返回所有<p>中的文本   ['段落文本', '第二段', '第三段']
print(root.xpath('//p//text()'))  #返回所有<p>中的文本   ['段落文本', '第二段', '第三段']


# # print(root.xpath('//div/text()'))
# print("="*50)
# print(root.xpath('//p[@class]')) #返回有class属性的标签，是Element的对象
# print("="*50)
# print(root.xpath('//p/@class')) #返回class的value   #/用来访问属性或方法
# print(root.xpath('//p[@role="listitem"]/@data-asin'))
# print("="*50)
# print(roo)

