<template>
	<view>
		<scroll-view scroll-with-animation scroll-y="true" style="width: 100%;">
			<!-- 用来获取消息体高度 -->
			<view id="okk" scroll-with-animation>
				<!-- 消息 -->
				<view class="flex-column-start">
					<!-- 机器人消息 -->
					<view class="flex-row-start margin-left margin-top one-show">
						<view class="chat-img flex-row-center">
							<image style="height: 75rpx;width: 75rpx;" src="../../static/image/robt.png"
								mode="aspectFit"></image>
						</view>
						<view class="flex" style="width: 500rpx;">
							<view class="margin-left padding-chat flex-column-start"
								style="border-radius: 35rpx;background-color: #f9f9f9;">
								<text style="word-break: break-all;">你好，我是ChatGPT助手。</text>
								<text style="word-break: break-all;">你前面还有{{queuenum}}个问题在排队～～～</text>
								<text style="word-break: break-all;">你在等待回答的问题:</text>
								<text style="word-break: break-all;" v-for="(question,i) in questions" :key="i">
									<text v-if="question['isAnswer']==0"> - {{question['question']}}</text>
								</text>
							</view>
						</view>
					</view>
				</view>

				<view class="flex-column-start" v-for="(x,i) in msgList" :key="i">
					<!-- 用户消息 头像可选加入-->
					<view v-if="x.my" class="flex justify-end padding-right one-show  align-start  padding-top">
						<!-- 	<image v-if="!x.my" class="chat-img" src="../../static/..." mode="aspectFill" ></image> -->
						<view class="flex justify-end" style="width: 400rpx;">
							<view class="margin-left padding-chat bg-cyan" style="border-radius: 35rpx;">
								<text style="word-break: break-all;">{{x.msg}}</text>
							</view>
						</view>
						<!-- <image class="chat-img margin-left" src="../../static/..." mode="aspectFill" ></image> -->
					</view>
					<!-- 机器人消息 -->
					<view v-if="!x.my" class="flex-row-start margin-left margin-top one-show">
						<view class="chat-img flex-row-center">
							<image style="height: 75rpx;width: 75rpx;" src="../../static/image/robt.png"
								mode="aspectFit"></image>
						</view>
						<view class="flex" style="width: 500rpx;">
							<view class="margin-left padding-chat flex-column-start"
								style="border-radius: 35rpx;background-color: #f9f9f9;">
								<text style="word-break: break-all;">{{x.msg}}</text>
							</view>
						</view>
					</view>
				</view>
				<!-- loading是显示 -->
				<view v-show="msgLoad" class="flex-row-start margin-left margin-top">
					<view class="chat-img flex-row-center">
						<image style="height: 75rpx;width: 75rpx;" src="../../static/image/robt.png" mode="aspectFit">
						</image>
					</view>
					<view class="flex" style="width: 500rpx;">
						<view class="margin-left padding-chat flex-column-start"
							style="border-radius: 35rpx;background-color: #f9f9f9;">
							<view class="cuIcon-loading turn-load" style="font-size: 35rpx;color: #3e9982;">

							</view>
						</view>
					</view>
				</view>
				<!-- 防止消息底部被遮 -->
				<view style="height: 130rpx;">

				</view>
			</view>

		</scroll-view>

		<!-- 底部导航栏 -->
		<view class="flex-column-center" style="position: fixed;bottom:0px;width: 100%;">
			<view class="bottom-dh-char flex-row-around" style="font-size: 55rpx;">
				<!-- vue无法使用软键盘"发送" -->
				<input v-model="msg" class="dh-input" type="text" style="background-color: #f0f0f0;" @confirm="sendMsg"
					confirm-type="search" placeholder-class="my-neirong-sm" placeholder="用一句简短的话描述您的问题" />
				<button @click="sendMsg" :disabled="msgLoad" class="btn bg-cyan round">发送</button>
			</view>
		</view>
	</view>
</template>

<script>
	import axios from 'axios';
	export default {
		onLoad() {
			let _this = this
			this.userId=localStorage.getItem("userId")
			// _this.userId = "17937ca4-ada1-11ed-9623-7e2a62d56ed6"
			_this.getQueueNums()
			_this.getAnswers()
			if (!_this.userId) {
				axios({
						method: "get",
						url: `${_this.url}/uuid`, // 接口地址
					})
					.then(response => {
						console.log(response, "success"); // 成功的返回
						_this.userId = response.data.uuid
						localStorage.setItem("userId", _this.userId)
						_this.getAnswers()
					})
					.catch(error => {

					}); // 失败的返回
			}
		},
		data() {
			return {
				url: "http://127.0.0.1:8080",
				queuenum: 0,
				queueInterval: '',
				answersetInterval: '',
				msgLoad: false,
				anData: {},
				userId: "",
				animationData: {},
				showTow: false,
				msgList: [],
				msgContent: "",
				msg: "",
				questions:[]
			}
		},
		methods: {
			getAnswers() {
				let _this = this
				if (!_this.userId) return
                _this.queueInterval = setInterval(() => {
                	axios({
                			method: "get",
                			url: `${_this.url}/answers?userId=${_this.userId}`, // 接口地址
                		})
                		.then(response => {
                			console.log(response, "success"); // 成功的返回
                			_this.questions=response.data.map(val=>JSON.parse(val))
							_this.msgList=[]
							_this.questions.forEach(val=>{
								if(val.isAnswer==1){
									_this.msgList.push({my:true,msg:val['question']})
									_this.msgList.push({my:false,msg:val['answer']})
								}
							})
                		})
                		.catch(error => {
                
                		}); // 失败的返回
                }, 3000)
			},
			getQueueNums() {
				let _this = this
				if (_this.queueInterval) return
				_this.queueInterval = setInterval(() => {
					axios({
							method: "get",
							url: `${_this.url}/counts`, // 接口地址
						})
						.then(response => {
							console.log(response, "success"); // 成功的返回
							_this.queuenum = response.data
						})
						.catch(error => {

						}); // 失败的返回
				}, 3000)
			},
			sendMsg() {
				let _this = this
				// 消息为空不做任何操作
				if (this.msg == "") {
					return 0;
				}
				this.msgList.push({
					"msg": this.msg,
					"my": true
				})
				this.msgContent = this.msg
				this.msgLoad = true
				// 清除消息
				this.msg = ""
				axios({
						method: "post",
						url: `${_this.url}/chat`, // 接口地址
						timeout: 1000 * 60 * 5,
						data: {
							prompt: this.msgContent, // 传接口参数
							userId:_this.userId
						}
					})
					.then(response => {
						console.log(response, "success"); // 成功的返回
						this.msgList.push({
							"msg": "你的问题正在排队中，请耐心等待",
							"my": false
						})
						// this.msgContent += ("openai:" + this.msg + "\n")
						this.msgLoad = false
					})
					.catch(error => {
						this.msgList.push({
							"msg": "服务器响应超时",
							"my": false
						})
						this.msgLoad = false
						console.log(error, "error")
					}); // 失败的返回
			},
			hideKey() {
				uni.hideKeyboard()
			},
		},
		beforeDestroy() {
			let _this = this
			if (_this.queueInterval) {
				clearInterval(_this.queueInterval)
				_this.queueInterval = ''
			}


		}
	}
</script>

<style>
	.bottom-dh-char {
		background-color: #f9f9f9;
		width: 100%;
		height: 110rpx;
	}

	.center-box {
		width: 720rpx;
		padding-left: 25rpx;
	}

	.btn {
		height: 90rpx;
		width: 20%;
	}

	.flex-row-start {
		display: flex;
		flex-direction: row;
		align-items: flex-start;
	}

	.hui-box {
		width: 750rpx;
		height: 100%;

	}

	.dh-input {
		width: 75%;
		height: 90rpx;
		border-radius: 100rpx;
		padding-left: 40rpx;
		margin-left: 20rpx;
		background-color: #FFFFFF;
	}

	.box-normal {
		width: 750rpx;
		height: 180px;
		background-color: #FFFFFF;
	}

	.tb-text view {
		font-size: 65rpx;
	}

	.tb-text text {
		font-size: 25rpx;
		color: #737373;
	}

	.chat-img {
		border-radius: 50%;
		width: 100rpx;
		height: 100rpx;
		background-color: #f7f7f7;
	}

	.padding-chat {
		padding: 17rpx 20rpx;
	}

	.tb-nv {
		width: 50rpx;
		height: 50rpx;
	}
</style>
