<template>
    <div id="login">
        <h1>관리자 로그인</h1>
        <div class="form-inputs">
            <label for="username"></label>
            <input type="text" id="username" name="username" v-model="input.username" placeholder="User ID" />
        </div>
        <div class="form-inputs">
            <label for="password"></label>
            <input type="password" id="password" name="password" v-model="input.password" placeholder="Password" />
        </div>
        <button type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>
    export default {
        name: 'Login',
        data() {
            return {
                input: {
                    username: "",
                    password: ""
                }
            }
        },
        methods: {
            login() {
                if(this.input.username != "" && this.input.password != "") {
                    // This should actually be an api call not a check against this.$parent.mockAccount
                    if(this.input.username == this.$parent.mockAccount.username && this.input.password == this.$parent.mockAccount.password) {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "Search" });
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
</style>