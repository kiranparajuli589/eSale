<template>
    <div class="row container">
        <div class="col"></div>
        <div class="col-md-4">
            <h1 class="page-title">LOGIN</h1>
            <form method="POST">
                <fieldset class="form-group">
                    <div id="div_id_username" class="form-group">
                <label for="id_username" class=" requiredField">
                    Email Address<span class="asteriskField">*</span>
                </label>
                <div class="">
                    <input type="text" name="username" autofocus autocapitalize="none"
                           autocomplete="username" maxlength="50"
                           class="textinput textInput form-control" required id="id_username">
                </div>
            </div>
                    <div id="div_id_password" class="form-group">
                <label for="id_password" class=" requiredField">
                    Password<span class="asteriskField">*</span>
                </label>
                <div class="">
                    <input type="password" name="password" autocomplete="current-password"
                           class="textinput textInput form-control" required id="id_password">
                </div>
            </div>
                </fieldset>
                <div class="form-group">
                    <router-link
                            to="/dashboard"
                            v-slot="{ href, route, navigate}"
                    >
                        <button :href="href" @click="navigate" class='btn btn-info'>
                            LOGIN
                        </button>
                    </router-link>
                    <small class="text-muted ml-2">
                        <a href="/accounts/password/reset/">Forgot Password?</a>
                    </small>
                </div>
            </form>
            <div class="border-top pt-3">
            <small class="text-muted">
                Need An Account? <a class="ml-2" href="/accounts/register/">Sign Up Now</a>
            </small>
        </div>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    import axios from "axios"
    export default {
        name: "Login",
        data() {
            return {
                isAuthenticated: false
            }
        },
        methods: {
            toHomePage() {
                this.$router.push({name:'home'})
            },
            // TODO
            // async onLinkClicked() {
                // let response = await axios.get("http://127.0.0.1/")
                // if (!isAuthenticated) {
                // }
            // },
            // submitForm() {
            // }
        }
    }
</script>

<style scoped>

</style>