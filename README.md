# server
WSN小车sink端运行的server

2020/11/13
1. 为了完成UWB定位，需要知道每一个UWB的GPS位置信息；
2. UWB每隔一段时间才发送距离信息给sink，sink进行三点定位时，取每一个UWB最近回传的距离信息来定位；
3. 地图绘制：经度[103.92388, 103.93755], 纬度[30.74216, 30.75348]

2020/11/27
1.完成了两个UWB的测试，本次测试还利用了惯导和惯导软件来直接读取软件中的GPS信息来表示UWB的位置。
    问题1. 两个UWB还是没办法定位；
    问题2. 惯导软件给的GPS与百度地图等地图给的GPS相差很大，惯导给的楼顶的GPS在地图上已经到了成都合院的位置；
    问题3. 逻辑上UWB的发送是0.5s发送一个message，一个message里面只有一个distance；但是实际上server偶尔会从一条message里
    收到多个distance；因此应对措施是用'#'作为间隔符，每一次读取一条message后，都只保留最后一个distance作为最新检测到的距离；
2.和惯导这边商量了具体的TCP包传输格式：message间用'#'号分隔，数据间用';'号分隔，数据内用','分隔；

2021/5/13
1.完成模块的分离和抽象，添加对每个小车的接收数据日志，添加对每次下发命令的发送日志。
2.完成单小车直线测试，在该测试中，给定一个 target gps，小车朝该位置移动。

2021/7/30
1.完善代码规范
2.完成三个小车对一个目标的跟踪，人拿着一个小车当作目标跟踪。
3.完成调度算法的预实现，目前正在三点定位算法测试
