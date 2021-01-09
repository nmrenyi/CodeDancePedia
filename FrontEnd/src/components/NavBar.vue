<template>
  <div class="menuBar" id="menuBar">
      <div class="menuLogo" @click="home"><img class="logo" :src="logo_url"><span>首页</span></div>
      <div class="signinInfo"><a @click="sign_in">{{signin_tip}}</a></div>
      <div class="signupInfo"><a @click="sign_up">注册</a></div>
      <div class="username">{{username}}</div>
      <el-dropdown class="userMenu">
          <div class="dropdownBTN"></div>
          <el-dropdown-menu slot="dropdown" class="dropdownContent">
              <el-dropdown-item><div class="dropdownContent" @click="user">用户信息</div></el-dropdown-item>
              <el-dropdown-item><div class="dropdownContent" @click="history">历史纪录</div></el-dropdown-item>
              <el-dropdown-item><div class="dropdownContent" @click="logout">退出登录</div></el-dropdown-item>
              <el-dropdown-item><div class="dropdownContent" @click="about">关于</div></el-dropdown-item>
          </el-dropdown-menu>
      </el-dropdown>
  </div>
</template>

<script>
    import Cookie from "@/utils/cookies"

    export default {
        name: 'NavBar',
        props: {
            name: {
                type: String,
                default: () => ""
            },
        },
        data() {
            return {
                username: "未登录",
                user_id: -1,
                signin_tip: "登录",
                logo_url : require('@/assets/logo.png')
            }
        },
        methods: {
            home() {
                this.$router.push('/')
            },
            sign_in() {
                if (this.signin_tip == "登录") {
                    this.$router.push('/sign_in')
                } else if (this.signin_tip == "登出") {
                    this.logout()
                }
            },
            sign_up() {
                this.$router.push('/sign_up')
            },
            logout() {
                Cookie.setCookie("username", '', 1)
                Cookie.setCookie("user_id", -1, 1)
                this.setSignStatus()
                this.$message.info('用户已登出')
                this.$router.push('/')
            },
            user() {
                this.setSignStatus()
                if (this.user_id < 0 || this.user_id == '') {
                    this.$message({
                        type: 'warning',
                        message: '您还未登录，无法查看用户主页'
                    });
                } else {
                    this.$emit("label_change", "user_management")
                    this.$router.push({
                        name: 'user',
                        params: {
                            label: "user_management"
                        }
                    })
                }
            },
            history() {
                this.setSignStatus()
                if (this.user_id < 0 || this.user_id == '') {
                    this.$message({
                        type: 'warning',
                        message: '您还未登录，无法查看历史纪录'
                    });
                } else {
                    this.$emit("label_change", "history")
                    this.$router.push({
                        name: 'user',
                        params: {
                            label: "history"
                        }
                    })
                }
            },
            about() {
                this.$router.push('/about')
            },
            setSignStatus() {
                // 设置用户名
                this.username = Cookie.getCookie("username")
                this.user_id = Cookie.getCookie("user_id")
                this.signin_tip = "登出"
                if (this.username == '') {
                    this.username = "未登录"
                    this.signin_tip = "登录"
                }
            }
        },
        created() {
            this.setSignStatus()
        },
        watch: {
            "name": {
                handler(value) {
                    this.username = value
                }
            }
        }
    }
</script>

<style scoped>
    div.menuBar {
        width: 100%;
        height: 60px;
        background-color: rgba(0, 0, 0, 1);
        opacity: 1.0;
        position: fixed;
        z-index: 100;
    }
    
    div.menuLogo {
        position: absolute;
        /* top: 30%; */
        width: 100px;
        height: 100%;
        left: 20px;
        color: aliceblue;
        cursor: pointer;
    }

    div.menuLogo span{
        position: absolute;
        top: 30%;
        left: 45px;
    }

    div.menuLogo span:hover{
        color: aqua;
    }

    img.logo{
        width: 40px;
        height: 40px;
        float: left;
        position: relative;
        top: 5px;
    }
    
    div.signinInfo a {
        text-decoration: none;
        position: absolute;
        right: 140px;
        top: 30%;
        color: aliceblue;
        cursor: pointer;
    }
    
    div.signinInfo a:hover {
        color: aqua;
    }
    
    div.signupInfo a {
        text-decoration: none;
        position: absolute;
        right: 80px;
        top: 30%;
        color: aliceblue;
        cursor: pointer;
    }
    
    div.signupInfo a:hover {
        color: aqua;
    }
    
    div.username {
        position: absolute;
        right: 205px;
        top: 30%;
        color: aliceblue;
    }

    .el-dropdown {
        vertical-align: top;
    }
    .el-dropdown + .el-dropdown {
        margin-left: 15px;
    }
    .el-icon-arrow-down {
        font-size: 12px;
    }
    
    .el-dropdown.userMenu {
        position: absolute;
        right: 5px;
        top: 20%;
        /* display: inline-block; */
    }
    
    div.dropdownBTN {
        width: 40px;
        height: 40px;
        background: url(../assets/hamburger.svg);
        background-repeat: no-repeat;
        border: none;
        cursor: pointer;
    }
    
    div.dropdownContent {
        width: 100%;
        margin-left: 15px;
        margin-right: 15px;
        font-size: 13pt;
    }
    
</style>