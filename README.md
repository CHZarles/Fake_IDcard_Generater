# Fake_IDcard_generater

1. 用于生成训练卡片分类器用，不要用作非法用途
2. 这里只生成了身份证背面，但实际上可以生成身份证正面，有需要的自己摸索一下。
3. 在 ./avater/....里面放头像的图片
4. 图片输出到 ./fake_back/..文件夹里
5. 头像采集自 https://thispersondoesnotexist.com/



# Usage

1. 在avater里放置头像材料，然后自己配置avatrt_path

![image-20210708173704706](https://i.loli.net/2021/07/08/lVwCEyiJv4XQ51N.png)

   

```
#dataGenerator.py
if __name__ == '__main__':
  	.........
        avater_path = r'./avater/'+str(random.randint(1, 3))+'.png' #随机选择路径
	.........
```



2.设置loop_num : loop_num = n -> 生成n张图片

```
#dataGenerator.py
if __name__ == '__main__':
  	........
    loop_num = 10
    for i in range(loop_num):
       ............
```
