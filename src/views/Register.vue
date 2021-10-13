<template>
    <div class="register">
        <h1>관리자 등록</h1>
            <div class="form-inputs">
                <label for="username"></label>
                <input type="text" id="username" name="username" v-model="input.username" placeholder="User ID" />
            </div>
            <div class="form-inputs">
                <label for="password"></label>
                <input type="password" id="password" name="password" v-model="input.password" placeholder="Password" />
            </div>
            <a href="#" class="btn-gradient-radius" onclick="register()">Register</a>
            <button type="button" v-on:click="register()">Register</button>
      </div>
</template>

<script>
    export default {
        name: 'Register',
        data() {
            return {
                input: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            register() {
                if(this.input.username != "" && this.input.password != "") {
                    // This should actually be an api call not a check against this.$parent.mockAccount
                    if(this.input.username == this.$parent.mockAccount.username && this.input.password == this.$parent.mockAccount.password) {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "Login" });
                    } else {
                        console.log("The username and / or password is incorrect");
                    }
                } else {
                    console.log("A username and password must be present");
                }
            }
        }
    }
</script>

<style>
    .form-inputs {
        padding-bottom: 10px;
    }
    .form-inputs label {
        padding-right: 10px;
    }
    .btn-gradient-radius {
        display: inline-block;
        padding: 7px 10px;
        border-radius: 25px;
        text-decoration: none;
        color: #fff;
        background-image: linear-gradient(45deg, #42b983 0%, #68be8d 100%);
        transition: .4s;
    }
    .btn-gradient-radius:hover {
        background-image: linear-gradient(45deg, #00a497 0%, #38b48b 100%);
    }
</style>