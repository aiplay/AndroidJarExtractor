### 基本作用

使用该工具，将指定的jar文件解压并进行反编译，并对反编译的结果进行分析。

1. 生成对应的tmp目录，里面存放 _class_ 目录、 _jad_ 目录和 _output_文件：

    > _class_ 目录存放jar中原始的class文件；

    > _jad_ 目录存放反编译的结果；

    > _output_ 记录哪些文件使用了哪些android接口，并记录调用行代码。

2. 运行 _execute.py_ 文件来使用该工具，同时传入jar所在的绝对路径。

	> 例如：python execute.py ~/test.jar

3. 目前该工具仅限在mac操作系统使用。