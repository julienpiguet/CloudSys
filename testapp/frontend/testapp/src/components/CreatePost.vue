<template>
    <v-card class="my-4 pa-2" elevation="2" outline>
        <v-row>
            <v-col>
                <v-img :src="previewImage" class="d-flex" />
                <input type="file" accept="image/jpeg" @change=uploadImage>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-form v-model="valid" @submit.prevent="send" class="mx-1">

                <div class="d-flex justify-space-around align-center flex-column flex-md-row">
                    <v-text-field class="align-center" v-model="title" :rules="titleRules" label="Title"
                        density="compact" variant="outlined" style="width: auto" single-line hide-details required>
                    </v-text-field>
                    <v-btn class="ml-1" @click="send" size="small" :disabled="!valid" elevation="0"  icon plain><v-icon :color="(valid ? 'blue' : '')" icon="mdi-upload"/></v-btn>
                </div>
                </v-form>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>

export default {
    name: 'ViewPost',
    data: () => ({
        valid: false,
        title: '',
        titleRules: [
            v => !!v || 'Title is required',
            v => (v && v.length <= 40) || 'Title must be less than 40 characters',
            v => !(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/).test(v) || 'Title must not contains special characters',
        ],
        previewImage:null
    }),

    methods: {
        send() {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: this.title, img: this.previewImage })
            };
            fetch("http://localhost:3000/element", requestOptions)
        },
        uploadImage(e){
                const image = e.target.files[0];
                const reader = new FileReader();
                reader.readAsDataURL(image);
                reader.onload = e =>{
                    this.previewImage = e.target.result;
                    console.log(this.previewImage);
                };
            }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
