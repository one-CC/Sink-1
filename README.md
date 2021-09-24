# Sink
WSN sink端运行的server程序

2020/11/13
1. 为了完成UWB定位，需要知道每一个UWB的GPS位置信息；
2. UWB每隔一段时间才发送距离信息给sink，sink进行三点定位时，取每一个UWB最近回传的距离信息来定位；
3. 地图绘制：经度[103.92388, 103.93755], 纬度[30.74216, 30.75348]

2020/11/27
1. 完成了两个UWB的测试，本次测试还利用了惯导和惯导软件来直接读取软件中的GPS信息来表示UWB的位置。
    1) 问题1: 两个UWB还是没办法定位；
    2) 问题2: 惯导软件给的GPS与百度地图等地图给的GPS相差很大，惯导给的楼顶的GPS在地图上已经到了成都合院的位置；
    3) 问题3: 逻辑上UWB的发送是0.5s发送一个message，一个message里面只有一个distance；但是实际上server偶尔会从一条message里
    收到多个distance；因此应对措施是用'#'作为间隔符，每一次读取一条message后，都只保留最后一个distance作为最新检测到的距离；
2. 和惯导这边商量了具体的TCP包传输格式：message间用'#'号分隔，数据间用';'号分隔，数据内用','分隔；

2021/5/13
1. 完成模块的分离和抽象，添加对每个小车的接收数据日志，添加对每次下发命令的发送日志。
2. 完成单小车直线测试，在该测试中，给定一个 target gps，小车朝该位置移动。

2021/7/30
1. 完善代码规范
2. 完成三个小车对一个目标的跟踪，人拿着一个小车当作目标跟踪。
3. 完成调度算法的预实现，目前正在三点定位算法测试

2021/9/8
1. 完成BIO到AIO的代码重构。
2. 将Sink项目的结构规范化。
3. 完成AIO下一辆小车追另一辆小车的测试（停顿时间大大降低），完成与后端通信的测试。

Next TODO: 
1. 节点选择算法存在缺陷
    1) 优化score的计算方式
    2) 节点选择时，应该过滤断开连接的节点
2. 当小车断开连接后，继续向该小车发送消息，将造成NPE
    1) 小车发消息前应该做空指针判断
3. 优化小车是否已连接的判断、断开连接的处理
    1) 对已连接的判断还加上是否已经有数据上行
    2) 断开连接时，将Car对象的属性初始化

Future TODO: 
1. Sink应用层上的心跳机制：一定时长内没有收到上行时，断开连接，取消Task
2. 小车的运动方式改为连续运动，而不是基于指令（需要注意速度）