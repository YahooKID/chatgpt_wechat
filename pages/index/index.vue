<template>
	<view class="bg">
		<scroll-view scroll-with-animation :scroll-y="isScroll" :scroll-top="scrollTop" style="width: 100%;">
			
			<!-- 用来获取消息体高度 -->
			<view id="okk" scroll-with-animation>
				<!-- 消息 -->
				<view class="flex-column-start" v-for="(x,i) in msgList" :key="i">
					<!-- 用户消息 头像可选加入-->
					<view v-if="x.my" class="userinfo">
						<view class="flex justify-end my-info">
							<view class="usermsg" style="max-width: 500rpx;">
								<text style="word-break: break-all;" selectable='true'>{{x.msg}}</text>
							</view>
							<view class="chat-img" style="margin-left:20rpx ;">
								<image style="height: 100rpx;width: 100rpx;" :src="userAvatar" mode="aspectFit">
								</image>
							</view>
						</view>
					</view>
					<!-- 机器人消息 -->
					<view v-if="!x.my" class="aiinfo">
						<view class="chat-img ">
							<image style="height: 100rpx;width: 100rpx;" src="../../static/openai1.png" mode="scaleToFill">
							</image>
						</view>
						<view class="flex" style="max-width: 500rpx;">
							<view class="aimsg" style="border-radius: 35rpx;background-color: #f9f9f9;">
								<text style="word-break: break-all;">{{x.msg}}</text>
								
							</view>
						</view>
					</view>
				</view>
				<!-- 防止消息底部被遮 -->
				<view style="height: 260rpx;">
				</view>
			</view>
		</scroll-view>
		<!-- 底部导航栏 -->
		<view class="flex-column-center"><view class="inpubut" z-else>
	</view>
			<view class="inpubut">
				<input v-model="msg" class="dh-input" type="text" @confirm="sendMsg" confirm-type="search"
					placeholder-class="my-neirong-sm" placeholder="你想说什么" @blur="isScroll=true;" @focus="isScroll=false;"/>

				<button @click="sendMsg" :disabled="msgLoad" class="btn">{{isRequesting?'请求中...':sentext}}</button>
				
			</view>
		</view>
		
	</view>
</template>

<script>
	import md5 from "./md5.js"
	export default {
		data() {
			return {
				scrollTop:9999,
				isScroll:true,//是否可以滑动
				userAvatar: '../../static/user.png',//头像
				apiurl: '',
				apisucc: false,
				apibut: '...',
				msgLoad: true,
				isRequesting:true,
				msgList: [{
					my: false,
					msg: "欢迎使用chatGPT"
				}],
				token: "",
				msgContent: "",
				msg: "",
				tempmsg: "",
				infos:"",
				isfirst: true
			}
		},
		computed:{
			sentext:function(){
				return `发送`
			}
		},
		onLoad() {
		
			const that = this;
			if (uni.getStorageSync('user-avatar') !== undefined){
				this.userAvatar = uni.getStorageSync('user-avatar')
			}
			uni.request({
				url: this.apiurl,
				method: 'GET',
				success: (res) => {
						this.msgLoad = false;
						this.isRequesting = false;
					},
				fail:(err) => {
					this.msgLoad = true;
					this.isRequesting = true;
					this.msgList.push({
						my: false,
						msg: "网络异常，请重启小程序重试",
						
					})
				}
			})
			

		},
		methods: {
			clopop() {
				this.$refs.popup.close('center')
			},
			openpop() {
				this.$refs.popup.open('center')
			},

			sendMsg() {
				if (this.msg == "") {
					return 0;
				}
				console.log(this.token)
				this.msgContent += ('YOU:' + this.msg + "\n")
				this.isRequesting=true;
				this.msgList.push({
					"msg": this.msg,
					"my": true
				})
				this.tempmsg = this.msg;
				this.msgContent += ('YOU:' + this.msg + "\n")
				console.log(this.msgContent);
				this.msgLoad = true
				this.msg = ""
				if(this.isfirst){
					uni.request({
						url: this.apiurl+"/amionline?cc="+this.tempmsg,
						method: 'GET',
						success: (res) => {
								if(res.data.length>5)
								{
								this.msgList.push({
									my: false,
									msg: "认证成功，是正确的人！",	
								})
								this.token = md5.hex_md5(res.data)
								this.msgLoad = false;
								this.isRequesting = false;
								this.isfirst=false;
								}
								else{
									this.msgLoad = true;
									this.isRequesting = true;
									this.msgList.push({
										my: false,
										msg: "网络异常，请重启小程序重试",	
									})
								}
							},
						fail:(err) => {
							this.msgLoad = true;
							this.isRequesting = true;
							this.msgList.push({
								my: false,
								msg: "网络异常，请重启小程序重试",	
							})
						}
					})
				}
				else{
				uni.request({
					url: this.apiurl+"/get_chatgpt?token="+this.token+"&message="+this.tempmsg,
					method: 'GET',
					success: (res) => {
						//if (res.data.code == 200) {
							let text = res.data
							console.log(text);
							this.msgList.push({
								"msg": text,
								"my": false
							})
							this.isRequesting=false;
							this.msgLoad=false;
							this.msgContent += (text + "\n")
							this.scrollToBottom()
					},
					fail: (err) => {
						console.log(3344444,'失败');
					}
				})

			}
			},
			scrollToBottom(){
				const that=this;
				setTimeout(()=>{
					that.scrollTop++
				},500)
			},
		}
	}
</script>

<style>
	page {
		height: 100%;
	}
	.bg {
		width: 100%;
		height: 100%;
	}

	.bg-img {
		width: 100%;
		height: 100%;
		position: fixed;
	}

	.userinfo {
		animation: oneshow 0.8s ease 1;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		padding-right: 20rpx;
		margin-top: 20rpx;
	}

	.usermsg {
		margin-left: 20rpx;
		padding: 17rpx 20rpx;
		border-radius: 35rpx;
		background-color: #f9f9f9 !important;
		/*margin-top: 20rpx;*/
	}

	.my-info {
		display: flex;
		align-items: center;
	}

	.aiinfo {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-left: 20rpx;
		margin-top: 20rpx;
		animation: oneshow 0.8s ease 1;
	}

	.chat-img {
		overflow: hidden;
		border-radius: 50%;
		/* width: 100rpx;
		height: 100rpx; */
		background-color: #f7f7f7;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
	}

	.aimsg {
		display: flex;
		flex-direction: column;
		justify-content: center;
		margin-left: 20rpx;
		padding: 17rpx 20rpx;
	}

	.flex-column-center {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		position: fixed;
		bottom: 0px;
		width: 100%;
	}

	.inpubut {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: center;
		/* background-color: #f9f9f9; */
		width: 100%;
		height: 110rpx;
		font-size: 40rpx;
		margin-bottom: 20rpx;
	}

	.dh-input {
		width: 90%;
		height: 80rpx;
		border-radius: 100rpx;
		padding-left: 40rpx;
		margin-left: 20rpx;

		background-color: #f0f0f0;
	}

	.my-neirong-sm {
		font-size: 32rpx;
		color: #616161;
	}

	.btn {
		height: 80rpx;
		line-height: 80rpx;
		width: 35%;
		background: linear-gradient(to right, #008FFF, #29C8FC);
		color: #ffffff;
		font-size: 32rpx;
		;
		border-radius: 2500px;
		margin: 0 20rpx;

	}

	.popcls {
		width: 80vw;
		height: 40vh;
		background: white;
		border-radius: 20rpx;
		display: flex;
		flex-direction: column;
		justify-items: center;
		align-items: center;



	}
</style>
