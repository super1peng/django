#coding:utf-8

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

@python_2_unicode_compatible
class Category(models.Model):
    """
    Django 要求模型必须继承models.Model类
    Category 只需要一个简单的分类名name就可以了
    CharField 指定了分类名name的数据类型 CharField是字符型
    CharField 的max_length 参数指定其最大长度，超过这个长度就不能存入
    当然Django 还为我们提供了多种其他的数据类型，日期时间类型DateTimeField、整数类型IntegerField等等
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签 Tag 也比较简单，与Category一样
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100)
       
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    """
    文章的数据库表复杂，设计的字段更多
    """

    #文章标题
    title = models.CharField(max_length=70)
    
    #文章的正文，使用了TextField
    #存储比较短的字符串可以使用CharField，但是文章的正文是一段较大的文本，因此使用TextField
    body = models.TextField()

    #分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DateTimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章的摘要，可以没有文章的摘要，但是默认情况下CharField要求我们必须存入数据，不然就会报错
    #指定 CharField 的blank = True 参数值后就可以允许是空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    #这个是分类与标签，模型我们在上面已经定义过了
    #在这里把文章对应的数据库表和分类、标签对应的数据库表关联起来，但关联的形式稍微有点不同
    #规定一篇文章只能对应一个分类，但是一个分类下可以可能有很多篇文章，所以使用的是ForeignKey，即一对多的关联关系
    #对于标签来说，一篇文章可以有多个标签，同时一个标签下也可以多篇文章，所以使用ManyToManyField,表示这是多对多的关联关系
    #同时规定文章可以没有标签，因此为标签tags指定了blank = True
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    #文章作者，这里User是从 django.contrib.auth.models 导入的
    #django.contrib.auth 是django 内置的应用，专门用于处理网站用户注册、登录等流程，User是Django 为我们已经写好的用户模型
    #我们通过 ForeignKey 把文章和 User 关联起来。
    #因为我们规定一篇文章只能有一个作者，而一个作者可能会有多篇文章，因此是一对多的关联关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    #自定义 get_absolute_url 方法
    #记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})
# Create your models here.
