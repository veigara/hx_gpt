### 一、项目相关

goole邮箱：a1126680959@gmail.com
openai:https://chat.openai.com/auth/login
项目地址：svn://120.24.72.134/svn/project/java
用户名：zhx
密码：123456
swagger:http://localhost:9099/swagger-ui/index.html

邮箱：zhouhongxin@altener.cn
密码：181010

服务器：120.24.72.134  密码：Hndk2018

服务器2：47.108.184.22	root 密码:Hndk2018
mysql数据库	用户名密码	root	HNDK2018@cq
数据库服务器: 47.108.49.109    root        Hndk@2018

正式服务器：
mysql: 47.108.49.109:3306
tdengine:47.108.49.109:6041
redis:47.108.49.109:6379

本地站控：
192.168.128.120
hndk01 hndk2018
切换root账号：sudo -i

http://47.108.184.22:9095/ 
jenkins管理页面 用户名：admin  密码：admin

阿里云服务器管理：
登录名：重庆峘能电动车科技
密码：hndk2018

kafka监控
地址：http://47.108.184.22:8048/  账号：admin 密码：hndk2018

时序数据库Tdengine
地址：jdbc:TAOS-RS://47.108.184.22:6041/test
账号： root  密码: HNDK2018@cq
修改用户密码：alter user root pass 'HNDK2018@cq';
修改数据库参数：ALTER DATABASE db_hndk_station_relast CACHEMODEL 'both'  CACHESIZE 500
备份数据库：taosdump -h 127.0.0.1  -u root   -pHNDK2018@cq -o /root/back  -D db_hndk_station_relast
恢复数据库：taosdump -h 127.0.0.1 -u root -pHNDK2018@cq -i /root/back -T 8 -D db_hndk_station_relast
添加字段：ALTER STABLE  db_hndk_station.service_data_battery_cell_detail ADD COLUMN category int;
获取监控指标: http://47.108.184.22:6041/metrics
web 数据库面板：http://47.108.49.109:6060/login
hndk hndk2018 只读权限
# 当时序数据库不可用时，通过查询连接，在杀死 
终止连接(需要重启所连接的业务服务器)
KILL CONNECTION conn_id;
conn_id 可以通过 SHOW CONNECTIONS 获取。

终止查询
docker exec -it tdengine bash
taos -pHNDK2018@cq

<!--显示当前系统中正在进行的查询>
SHOW QUERIES;
<!--终止查询-->
KILL QUERY 'kill_id';

# 黑窗口输入查询
KILL QUERY 'kill_id';
kill_id 可以通过 SHOW QUERIES 获取。

禅道 120.24.72.134:9999 管理账号：admin 密码：Hndk2018   zhouhongxin 123456
微信商户操作密码：489652
http://47.108.184.22:9098/carBattery/cell_detail/detaill_export?query=%7B%22createTimeStart%22%3A%222023-04-19%2012%3A00%22%2C%22createTimeEnd%22%3A%222023-04-19%2023%3A59%22%7D&fileName=%E8%BD%A6%E8%BE%86%E8%BF%90%E8%A1%8C%E6%95%B0%E6%8D%AE1681891341471&

rancher1
高德地图子账号：HndkZhouHongXin@1167078043 密码：hndk2018

maven中心仓库地址：
https://issues.sonatype.org/secure/Signup!default.jspa
#推送的jar
https://s01.oss.sonatype.org/
账号：zhouhongxin  密码：ZhX4356289743@

七牛云
18102325010 Hndk2018!@#

kafka监控平台 http://47.108.184.22:8048/ 账号：admin 密码：hndk2018

云快冲充电桩管理密码：123456


站控系统svn
前端：svn://120.24.72.134/svn/project/NBAC/station-control/station-control-font
后端：svn://120.24.72.134/svn/project/NBAC/station-control/station-control-server


测试工控机地址192.168.2.102   用户名：cc   密码：abc.123

********************************************密码*****************************************************
充电机密码：691961
空压机密码：用户密码:9999 厂家密码:1226
agv充电机密码：...
云快充充电桩密码:123456
盛宏充电桩密码:080808
*************************************************************************************************
# 手动拉取镜像
docker pull docker.registry.cyou/tdengine/tdengine:3.3.1.0
docker pull docker.registry.cyou/library/openjdk:8-jdk
// docker 源
{ "registry-mirrors" :["https://docker.m.daocloud.io", "https://noohub.ru",
"https://huecker.io""https://dockerhub.timewebcloud"]}
# 强制更新镜像
docker-compose up -d --build hndk-admin

# 查看tdengine的详细执行计划
explain verbose true select last_row(*),station_id from db_hndk_station_relast.service_data_electricity_meter

select * from service_data_station where data_type='1' and create_time>='2024-06-24 11:26:35' and 
create_time<='2024-06-24 11:26:37' and data_content   LIKE '%\"chargingState\": \"3\"%'
 and station_id='ATH3-023003'order by create_time desc
 
# tdengine 监控
http://192.168.2.177:3000/
# tdengine 页面地址
http://47.108.49.109:6060/login

4g协议变更至v2.1
Car9993Request
ServiceDataBattery9993DetailExcel
ServiceDataBattery9993Vo
ServiceDataBattery9993
ServiceDataBattery9993ServiceImpl

select station_id,cabinet_id,min(charging_power_start),max(charging_power_end),ROUND(sum(period_falg4),2) as '尖',ROUND(sum(period_falg1),2) as '峰',ROUND(sum(period_falg2),2) as '平', ROUND(sum(period_falg3),2) as '谷',ROUND(sum(charge_capacity_meter),2) as '用电量',ROUND(sum(charge_capacity),2) as '累计电池补充电量' from service_data_battery_statistics where warehousing_time>='2024-08-01 00:00:00' and warehousing_time<='2024-08-31 23:59:59'
GROUP BY station_id,cabinet_id
### 二、java插件库
SHOUDONG 

### 三、前端知识库

#### 3.1 vue接收超出19位数的数字类型精度都是

```javascript
import  jsonBigint from 'json-bigint'
在axios配置文件
/解决前端处理19位精度丢失
instance.defaults.transformResponse = [
    function (data) {
        const json = jsonBigint({
            storeAsString: true
        })
        const res = json.parse(data)
        return res
    }
]
或者后台直接转为字符串
@JsonFormat(shape = JsonFormat.Shape.STRING)

```



### 四、知识库

#### 4.1 springboot相关

##### 4.1.1 SpringApplication的生命周期

```java
#发生顺序如下
ApplicationStartingEvent //在SpringApplication对象的初始化和监听器的注册之后，抛出的
ApplicationEnvironmentPreparedEvent//这个事件在Environment对象创建之后，Context对象创建之前，抛出
ApplicationContextInitializedEvent//这个事件在ApplicationContext对象被初始化后抛出，抛出的时候，所有bean的定义还没被加载
ApplicationPreparedEvent//这个事件在bean定义被加载之后，Context对象刷新之前抛出。
ApplicationStartedEvent//这个事件在Context对象刷新之后，应用启动器被调用之前抛出。
ApplicationReadyEvent//这个事件在应用启动器被调用之后抛出，这个代表着应用已经被正常的启动，可以接收请求了
ApplicationFailedEvent//这个事件只有在应用启动出现异常，无法正常启动时才会抛出。
```

基于生命周期，自定义监听器案例

```java
public class ApplicationContextInitializedEventListener implements ApplicationListener<ApplicationContextInitializedEvent> {
    @Override
    public void onApplicationEvent(ApplicationContextInitializedEvent applicationContextInitializedEvent) {
        System.out.println("ApplicationContextInitializedEvent");
    }
}
```

4.1.2 常用注解

```java
@SpringBootApplication

替代 @SpringBootConfiguration、@EnableAutoConfiguration、@ComponentScan

2、@ImportAutoConfiguration

导入配置类，一般做测试的时候使用，正常优先使用@EnableAutoConfiguration 

3、@SpringBootConfiguration

替代@Configuration

4、@ImportResource

将资源导入容器

5、@PropertySource 

导入properties文件

6、PropertySources

@PropertySource 的集合

7、@Role

bean角色定义为ROLE_APPLICATION(默认值)、ROLE_SUPPORT(辅助角色)、ROLE_INFRASTRUCTURE(后台角色，用户无感)
8、@Scope

指定bean的作用域，默认singleton，其它包括prototype、request、session、globalSession

9、@Lazy

使bean懒加载，取消bean预初始化。

10、@Primary

自动装配时当出现多个Bean候选者时，被注解为@Primary的Bean将作为首选者，否者将抛出异常。

11、@Profile

指定Bean在哪个环境下被激活

12、@DependsOn

依赖的bean注册完成，才注册当前类，依赖bean不存在会报错。用于控制bean加载顺序

13、@PostConstruct

bean的属性都注入完毕后，执行注解标注的方式进行初始化工作

14、@Autowired

默认按类型装配，如果我们想使用按名称装配，可以结合@Qualifier注解一起使用。

15、@Lookup

根据方法返回的类型，去容器中捞出对应

16、@Qualifier

申明bean名字，且可以按bean名字加载bean

17、@Required

检查bean的属性setXXX()方法，要求属性砸死配置阶段必须已配置

18、@Description

添加bean的文字描述

19、@EnableAspectConfiguration

启动AspectJ自动配置

20、EnableLoadTimeWeaving

启动类加载器动态增强功能，使用instrumentation实现

21、@AutoConfigurationPackage

包含该注解的package会被AutoConfigurationPackages注册

22、@AutoConfigureBefore

在指定配置类初始化前加载

23、@AutoConfigureAfter

在指定配置类初始化后加载

24、@AutoConfigureOrder

指定配置类初始化顺序，越小初始化越早

25、@ModelAttribute

26 选择器
@Conditional，当指定的条件都满足时，组件才被注册
@ConditionalOnBean，指定bean在上下文中时，才注册当前bean。用在方法上，则默认依赖类为方法的返回类型
@ConditionalOnClass，指定类在classpath上时，才初始化当前bean。用在方法上，则默认依赖类为方法的返回类型
@ConditionalOnCloudPlatform，在指定云平台才注册配置
@ConditionalOnExpression，指定spel为true时注册配置
@ConditionalOnJava，在指定java版本时注册配置
@ConditionalOnJndi
@ConditionalOnMissingBean，指定bean不在上下文中时，才初始化当前bean。用在方法上，则默认依赖类为方法的返回类型
@ConditionalOnMissingClass，指定类不在classpath上时，才初始化当前bean。用在方法上，则默认依赖类为方法的返回类型
@ConditionalOnNotWebApplication，不是在web环境才注册配置
@ConditionalOnProperty，配置文件中的值与指定值是否相等，相等才注册配置
@ConditionalOnResource，指定resources都在classpath上才注册配置
@ConditionalOnSingleCandidate，上下文中只有一个候选者bean时才注册配置
@ConditionalOnWebApplication，是在web环境才注册配置

27定时器
@EnableScheduling，开启定时任务功能
@Scheduled，按指定执行周期执行方法
@Schedules，包含多个@Scheduled，可同时运行多个周期配置
@EnableAsync，开启方法异步执行的能力，通过@Async或者自定义注解找到需要异步执行的方法。通过实现AsyncConfigurer接口的getAsyncExecutor()和getAsyncUncaughtExceptionHandler()方法自定义Executor和异常处理。
@Async，标记方法为异步线程中执行

28 注入配置文件properties
@EnableConfigurationProperties，启动@ConfigurationProperties功能
@ConfigurationProperties，将properties文件里的内容，自动注入bean对应的属性中
@DeprecatedConfigurationProperty，用在配置文件的getter()方法上，标记字段已经过期，并提示替换的字段。一般给spring-boot-configuration-processor使用。
@NestedConfigurationProperty，标记在配置文件的字段上，提示spring-boot-configuration-processor，配置包含嵌套的配置。
spring-configuration-metadata.json 提供配置的元信息，在写properties配置时，会有语法提示。在项目中引入spring-boot-configuration-processor项目，会扫描@ConfigurationProperties注解，自动生成spring-configuration-metadata.json

29 导入配置文件
@PropertySource
@PropertySource(value = {"classpath:xxxx/xxxx.properties"})//引入单个properties文件
@PropertySource(value ={"classpath:xxxx/xxxx.properties","classpath:xxxx/xxxx.properties"})//引入多个properties文件
@ImportResource //导入xml配置文件 可以分为两种模式，相对路径的classpath，绝对路径的file。
@Import导入额外的配置文件 //功能类似XML配置的，用来导入配置类，可以导入带有@Configuration注解的配置类或实现了ImportSelector/ImportBeanDefinitionRegistrar。
@SpringBootApplication
@Import({SmsConfig.class})
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

30事务注解
@Transactional

在Spring中，事务有两种实现，分别是编程式事务和声明式事务。

编程式事务：

编程式事务使用TransationTemplate或者直接使用底层的PlatformTransactionManager。对于编程式事务，spring推荐使用TransationTemplate。

声明式事务：

建立在AOP基础上，其本质是对方法前后进行拦截，然后再目标方法开始之前创建或者加入一个事务，在执行完目标方法之后根据执行情况提交或者回滚事务，通过@Transactional就可以进行事务操作，更快捷而且简单。推荐使用。

31 @ControllerAdvice //全局异常处理


```

#### 4.2 mybatis相关

##### 4.2.1 一对一，一对多字段映射

```java
//一对多
<resultMap id="monitorResultMap" type="com.hndk.assetInfo.vo.AssetInfoStationInfoChargMonitorVo">
        <result property="id" column="id"/>
        <result property="bid" column="bid"/>
        <result property="stationId" column="station_id"/>
        <result property="stationName" column="station_name"/>
        <result property="stationType" column="station_type"/>
        <result property="stationProvince" column="station_province"/>
        <result property="stationCity" column="station_city"/>
        <collection property="cabinetList" column="station_id" javaType="java.util.ArrayList"
            ofType="com.hndk.stationService.vo.ServiceDataMonitorCabinetVo"
            select="com.hndk.stationService.dao.ServiceDataCabinetMapper.getDataByStation" ></collection>
        <collection property="
  " column="station_id" javaType="java.util.ArrayList"
                    ofType="com.hndk.stationService.vo.ServiceDataBmsBrieflyVo"
                    select="com.hndk.stationService.dao.ServiceDataBmsMapper.getListBrieflyByStation" ></collection>
    </resultMap>
    
//一对一，多字段映射
  <resultMap id="monitorBaseResult" type="com.hndk.stationService.vo.ServiceDataMonitorCabinetVo">
        <result property="id" column="id"/>
        <result property="bid" column="bid"/>
        <result property="stationId" column="station_id"/>
        <result property="chargId" column="charg_id"/>
        <result property="batchId" column="batch_id"/>
        <result property="cabinetId" column="cabinet_id"/>
        <result property="cabinetStatus" column="cabinet_status"/>
        <association property="bmsVo"  column="{cabinetId=cabinet_id,stationId=station_id}"
                     javaType="com.hndk.stationService.vo.ServiceDataMonitorBmsVo"
                    select="com.hndk.stationService.dao.ServiceDataBmsMapper.getDetailByCabinet"></association>
        <association property="watercooledVo"  column="{cabinetId=cabinet_id,stationId=station_id}"
                     javaType="com.hndk.stationService.vo.ServiceDataWatercooledVo"
                    select="com.hndk.stationService.dao.ServiceDataWatercooledMapper.getDetailByCabinet"></association>
    </resultMap>
```

4.2.2 常用标签

| 标签                          | 说明          | 例子                                       |
| --------------------------- | ----------- | ---------------------------------------- |
| `select`                    | 定义查询语句      | `<select id="selectUser" parameterType="int" resultType="User">SELECT * FROM users WHERE id = #{id}</select>` |
| `insert`                    | 定义插入语句      | `<insert id="insertUser" parameterType="User">INSERT INTO users (name, age) VALUES (#{name}, #{age})</insert>` |
| `update`                    | 定义更新语句      | `<update id="updateUser" parameterType="User">UPDATE users SET name = #{name}, age = #{age} WHERE id = #{id}</update>` |
| `delete`                    | 定义删除语句      | `<delete id="deleteUser" parameterType="int">DELETE FROM users WHERE id = #{id}</delete>` |
| `if`                        | 条件判断        | `<select id="selectUsers" parameterType="User" resultType="User">SELECT * FROM users WHERE 1=1<if test="name != null"> AND name = #{name}</if><if test="age != null"> AND age = #{age}</if></select>` |
| `choose` `when` `otherwise` | 多条件判断       | `<select id="selectUsers" parameterType="User" resultType="User">SELECT * FROM users WHERE 1=1<choose><when test="name != null"> AND name = #{name}</when><when test="age != null"> AND age = #{age}</when><otherwise> AND 1=2</otherwise></choose></select>` |
| `where`                     | 用于拼接where子句 | `<select id="selectUsers" parameterType="User" resultType="User">SELECT * FROM users<where><if test="name != null"> AND name = #{name}</if><if test="age != null"> AND age = #{age}</if></where></select>` |
| `set`                       | 用于拼接set子句   | `<update id="updateUser" parameterType="User">UPDATE users<set><if test="name != null">name = #{name},</if><if test="age != null">age = #{age},</if></set>WHERE id = #{id}</update>` |
| `foreach`                   | 遍历集合        | `<select id="selectUsers" parameterType="java.util.List" resultType="User">SELECT * FROM users WHERE id IN<foreach collection="ids" item="id" open="(" separator="," close=")">#{id}</foreach></select>` |
| `resultMap`                 | 定义结果集映射关系   | `<resultMap id="userMap" type="User"><result property="id" column="user_id"/><result property="name" column="user_name"/><result property="age" column="user_age"/></resultMap>` |
| `result`                    | 定义属性映射关系    | `<result property="id" column="user_id"/>` |
| `association`               | 对象属性映射关系    | `<association property="address" javaType="Address"><result property="city" column="address_city"/><result property="street" column="address_street"/></association>` |
| `collection`                | 集合属性映射关系    | `<collection property="orders" ofType="Order"><result property="id" column="order_id"/><result property |

#### 4.3 mysql相关

##### 4.3.1 统计每隔半小时的数据
```sql
SELECT @rank:=@rank+1 AS rank_on,sum(charge_quantity_this_time),timse FROM (
SELECT charge_quantity_this_time,
DATE_FORMAT(CONCAT(DATE(r.`create_time`),' ',
HOUR(r.`create_time`),':',FLOOR(MINUTE(r.`create_time`)/30)*30),'%Y-%m-%d %H:%i') AS timse 
FROM service_data_chargingpile r 
ORDER BY timse) a, (SELECT @rank:= 0) b GROUP BY a.timse;
```
##### 4.3.2 计算当条数据与上一条的差值
```sql
select id,charge_quantity_this_time,current_meter_reading,meter_reading_before_charging,@a.po as pre, @a.po:=ROUND(a.current_meter_reading-a.meter_reading_before_charging,2) as cur from service_data_chargingpile a,(select @a.po:=0)s where id>1904 and id<1990 ;
```
#### 4.4 文件导出相关

##### 4.4.1 easypoi.base导出到模板，模板文件找不到

```java
#easypoi.base默认是读取当前FileLoaderImpl文件路径下resource下的路径，即必须在引用该jar包下模块中的resource里面才能找到
  fileis = FileLoaderImpl.class.getClassLoader().getResourceAsStream(url);
```

#### 4.5 Swagger 3注解

| 注解名称               | 作用                                   | 示例                                       |
| ------------------ | ------------------------------------ | ---------------------------------------- |
| @OpenAPIDefinition | 定义 OpenAPI 规范的元数据信息，如 API 的版本、服务器地址等 | `@OpenAPIDefinition(info = @Info(title = "API Demo", version = "1.0.0", description = "API 接口文档示例"))` |
| @Info              | 定义 API 文档的基本信息，如标题、描述、版本号等           | `@OpenAPIDefinition(info = @Info(title = "API Demo", version = "1.0.0", description = "API 接口文档示例"))` |
| @Server            | 定义 API 的服务器地址                        | `@Server(url = "http://localhost:8080")` |
| @Tag               | 定义 API 的标签，用于对 API 进行分类              | `@Tag(name = "用户管理")`                    |
| @Operation         | 定义 API 操作，如接口的名称、描述等                 | `@Operation(summary = "获取用户列表", description = "获取所有用户的列表")` |
| @Parameter         | 定义 API 参数，如参数名称、类型、描述等               | `@Parameter(name = "id", description = "用户ID", in = ParameterIn.PATH, required = true, schema = @Schema(type = "integer", format = "int64"))` |
| @RequestBody       | 定义 API 请求体，如请求参数的类型、描述等              | `@RequestBody(description = "请求参数", required = true, content = @Content(mediaType = "application/json", schema = @Schema(implementation = User.class)))` |
| @ApiResponse       | 定义 API 响应，如响应码、描述等                   | `@ApiResponse(responseCode = "200", description = "请求成功")` |
| @ApiResponses      | 定义多个 API 响应                          | `@ApiResponses({ @ApiResponse(responseCode = "200", description = "请求成功"), @ApiResponse(responseCode = "404", description = "请求的资源不存在")})` |
| @Schema            | 定义 API 返回值或请求参数的数据结构                 | `@Schema(type = "object", name = "User", description = "用户对象", properties = { @Property(name = "id", description = "用户ID", example = "1", required = true), @Property(name = "name", description = "用户名", example = "张三", required = true) })` |
| @Extension         | 定义扩展字段，用于添加自定义的元数据                   | `@Extension(name = "x-api-key", value = "123456")` |

#### 4.6  mybatis 映射报Cannot convert string 'xx' to java.sql.Timestamp value

```java
在检测映射类的类型没有错的情况下，可能是没有生成默认无参构造函数导致的报错
```



### 五、运维相关

#### 5.1、window 平台相关

##### 5.1.1 改变cmd平台utf-8字符集

```powershell
chcp 65001
```

##### 5.1.2 根据端口找应用

```shell
netstat -ano|findstr "8088"
```

##### 5.1.3 删除注册的服务

```powershell
sc delete redis  #删除redis服务
```

##### 5.1.4 注册redis服务

```powershell
redis-server.exe --service-install redis.windows.conf --loglevel verbose #注册redis服务
```



#### 5.2、centos平台相关

##### 5.2.1、防火墙

```shell
systemctl start firewalld      # 启动防火墙
systemctl status firewalld     # 查看防火墙状态
systemctl stop firewalld       # 关闭防火墙
systemctl disable firewalld    # 开启不启动防火墙
systemctl enable firewalld     # 开机启动防火墙
firewall-cmd --zone=public --list-ports            # 查询端口开放列表
firewall-cmd --zone=public --query-port=9200/tcp   # 查询具体端口是否开放
firewall-cmd --zone=public --add-port=9200/tcp --permanent     # 开放端口
firewall-cmd --zone=public --remove-port=9200/tcp --permanent  # 关闭端口
firewall-cmd --reload  
```

##### 5.2.2、开启远程登录

```shell
vim  /etc/ssh/sshd_config #找到PermitRootLogin 改为yes
service sshd restart #启动sshd服务。
```

##### 5.2.3、docker相关

###### 5.2.3.1、安装

阿里云官方镜像：https://developer.aliyun.com/mirror/

```sh
1.使用yum进行安装docker-ce
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3
sudo sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
# Step 4: 更新并安装Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start

# 注意：
# 官方软件源默认启用了最新的软件，您可以通过编辑软件源的方式获取各个版本的软件包。例如官方并没有将测试版本的软件源置为可用，您可以通过以下方式开启。同理可以开启各种测试版本等。
# vim /etc/yum.repos.d/docker-ce.repo
#   将[docker-ce-test]下方的enabled=0修改为enabled=1
#
# 安装指定版本的Docker-CE:
# Step 1: 查找Docker-CE的版本:
# yum list docker-ce.x86_64 --showduplicates | sort -r
#   Loading mirror speeds from cached hostfile
#   Loaded plugins: branch, fastestmirror, langpacks
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
#   docker-ce.x86_64            17.03.1.ce-1.el7.centos            @docker-ce-stable
#   docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
#   Available Packages
# Step2: 安装指定版本的Docker-CE: (VERSION例如上面的17.03.0.ce.1-1.el7.centos)
# sudo yum -y install docker-ce-[VERSION]
参考地址：https://developer.aliyun.com/mirror/docker-ce?spm=a2c6h.13651102.0.0.57e31b11dLCxM7

2.安装Docker Compose
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.11.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

docker-compose version #验证安装是否成功
参考地址：https://blog.csdn.net/qq_41929714/article/details/122692326
国内docker加速镜像：https://get.daocloud.io/ 

--restart=always  # 表示容器退出时，docker会总是自动重启这个容器
 
--restart=on-failure:3  # 表示容器的退出状态码非0(非正常退出)，自动重启容器，3是自动重启的次数。超过3此则不重启
 
--restart=no  # 默认值，容器退出时，docker不自动重启容器
 
--restart=unless-stopped  # 表示容器退出时总是重启，但是不考虑docker守护进程运行时就已经停止的容器

如果在创建容器的时候没有指定--restart参数，可以使用update更新容器
docker update --restart=always [container-name]

可用于查询镜像（Images）、容器（Containers）和本地卷（Local Volumes）等空间使用大户的空间占用情况。
docker system df
查看详细
docker system df -v
docker volume prune：删除无用的卷。
docker network prune：删除无用的网络

更改docker 默认储存位置
sudo vi /etc/docker/daemon.json
{
  "data-root": "/new/docker"
}
{
  "data-root": "/new/docker"
}

# docker 安装vim 
apt-get update
apt-get install vim
// 如果更新失败，修改下源
cat >/etc/apt/sources.list <<EOF
deb-src http://mirrors.aliyun.com/debian-security buster/updates main
deb http://mirrors.aliyun.com/debian/ buster main non-free contrib
EOF


sudo apt-get update时报错
chmod 777 /tmp
cd /tmp
```

# 拉去镜像超时
```
解决办法3.拉取镜像时，直接带上拉取镜像的加速地址

docker pull docker.mirrors.ustc.edu.cn/library/镜像名
```

# 利用docker history 查询镜像镜像信息来分析生成Dockerfile
```
可以查询镜像的环境参数设置等

docker history 48e4cf545b5a(image_id)

```
# 查看容器内线程的工作强度
top -Hp `pidof taosd`
 
#收到执行日志滚动
 sudo logrotate /etc/logrotate.d/check_restart_td.logrotate
 
#使用NTP服务可以自动同步宿主机和容器的时间
```
apt-get install ntp
# 启动NTP服务
sudo service ntp start
# 修改ntp.conf文件
$ vi /etc/ntp.conf

# 将服务器地址修改为宿主机的IP地址
server 192.168.0.100
```

# 清理 Docker Build 缓存
```
docker builder prune

```
# 手动同步时间
```
date -s "2023-04-08 14:18:00"   # 设置当前系统时间
hwclock --set --date "2023-04-08 14:18:00" 
```

# debian linux 修改时区，将utc修改为cst时区
```
 echo "export TZ='Asia/Shanghai'"  >> /etc/profile  
 cat /etc/profile |grep TZ  
 source /etc/profile
 date -R
 date 
```

###### 5.2.3.2 相关命令

```sh
systemctl restart docker #重启docker服务
systemctl enable docker #开机自启动
systemctl disable docker #关闭开机自启
systemctl status docker #查看服务状态

docker logs -f --tail 10 docker123 #要实时查看docker容器名为docker123的最新10行日志
docker exec -it 3a3afa942911 bash #使用docker exec进入容器内 3a3afa942911容器id/容器名称
docker inspect 容器名称 命令查看容器内的配置
docker stats 查询docker使用内存的
# 搜索结果前后20行的数据
 cat total.log |grep "收到充电桩对后台下发的充电桩开启充电控制应答结果" -a -C 20
```

##### 5.2.4 查找端口占用

```sh
netstat -tunlp |grep  8080 #查找8080端口
```

##### 5.2.5 nginx 相关命令

```sh
启动服务：nginx
退出服务：nginx -s quit
强制关闭服务：nginx -s stop
重载服务：nginx -s reload　　（重载服务配置文件，类似于重启，但服务不会中止）
验证配置文件：nginx -t
使用配置文件：nginx -c "配置文件路径"
使用帮助：nginx -h
```

##### 5.2.6 查看文件夹内文件大小

```shell
du -sh *
```

##### 5.2.7 查看磁盘空间占用情况

```shell
df -h
```

##### 5.2.8 jenkins相关

1. 批量删除构建记录

   ```shell
   在系统管理-->Script Console 中执行
   def jobName = "hndk-vue"   //删除的项目名称
   def maxNumber = 64    // 保留的最小编号，意味着小于该编号的构建都将被删除
    
   Jenkins.instance.getItemByFullName(jobName).builds.findAll {
     it.number <= maxNumber
   }.each {
     it.delete()
   }
   ```
#### 5.2.9 查看文件内各文件的大小
```shell
du -h -x --max-depth=1
```
#### 5.2.10 查看oom日志
```shell
#docker容器报137
journalctl -k | grep -i -e memory -e oom
```
#### 5.2.10 清空文件内容
```shell
truncate -s 0 /root/zj/docker/fast-boot/server/logs/total.log

#### 5.2.11 截取日志
```shell
sed -n '/2023-12-26 14:10:00/,/2023-12-26 14:11:00/p' total.log >> total1226.log 
```

#### 5.2.12 查找java程序
```shell
 ps -ef|grep java
```

#### 5.2.13 Ubuntu执行脚本命令
```shell
 bash start_control.sh
```
#### 5.2.14 Ubuntu 自动启动执行脚本命令
```shell
 cd /etc/systemd/system
 # 创建启动脚本服务
 [Unit]
Description=chargingcontrol application
After=network.target
[Service]
User=root
WorkingDirectory= /home/hndk01/java/chargercontrol
ExecStart= /home/hndk01/java/chargercontrol/run_control_ubuntu.sh start
ExecStop= /home/hndk01/java/chargercontrol/run_control_ubuntu.sh stop
TimeoutSec=10
RemainAfterExit=yes
GuessMainPID=no
#Restart=always
#RestartSec=3s
#User=root

[Install]
#WantedBy=multi-user.target
WantedBy=default.target

#启动服务
sudo systemctl enable chargingcontrol.service
sudo systemctl start chargingcontrol.service
```