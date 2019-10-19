"""对不同标签、特殊标记的处理程序"""


class Handler:
    """这是一个能够对原始文本进行操作的类
    是不同标记语言的基类
    里面编写了start()、end()、sub()三个函数以对原始文本进行统一的三种操作
    来转换成不同语言标记的格式（如HTTMl、XML），具体转化成什么形式取决于它子类中对标签的描述
    但不管要转换成什么样的语言标记形式，都统一依靠这三个方法完成，主不过为不同的语言标记编写的子类
    标签和特殊标志的内容是不一样的
    其中callback是一大亮点,提高了可拓展性
    start和end主要是为块添加标签的
    sub是通过正则表达式为块内容更换相应语言的的元素标记的
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                return match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    """这就是具体的HTML格式生成的子类，里面会包含基类中定义的三个具体操作方法
    还会为此语言格式建立具体的标签
    """
    @staticmethod
    def start_document():
        print('<html><head><title>...</title></head><body>')

    @staticmethod
    def end_document():
        print('</body></html>')

    @staticmethod
    def start_paragraph():
        print('<p>')

    @staticmethod
    def end_paragraph():
        print('</p>')

    @staticmethod
    def start_heading():
        print('<h2>')

    @staticmethod
    def end_heading():
        print('</h2>')

    @staticmethod
    def start_list():
        print('<ul>')

    @staticmethod
    def end_list():
        print('</ul>')

    @staticmethod
    def start_listitem():
        print('<li>')

    @staticmethod
    def end_listitem():
        print('</li>')

    @staticmethod
    def start_title():
        print('<h1>')

    @staticmethod
    def end_title():
        print('</h1>')

    @staticmethod
    def sub_emphasis(match):
        """与后面过滤器中的正则表达式结合使用，会把含有对应编组的match传进来
        """
        return '<em>{}</em>'.format(match.group(1))

    @staticmethod
    def sub_url(match):
        """与后面过滤器中的正则表达式结合使用，会把含有对应编组的match传进来
        """
        return '<a href="{}">{}</a>'.format(match.group(1), match.group(1))

    @staticmethod
    def sub_mail(match):
        """与后面过滤器中的正则表达式结合使用，会把含有对应编组的match传进来
        """
        return '<a href="mailto:{}">{}</a>'.format(match.group(1), match.group(1))

    @staticmethod
    def feed(data):
        print(data)
