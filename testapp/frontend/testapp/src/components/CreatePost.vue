<template>
    <v-btn class="ml-2" color="primary" dark @click.stop="dialog = true">
        New Item
    </v-btn>
    <v-dialog v-model="dialog" max-width="960">
        <v-card class="my-4 pa-2" elevation="2" outline>
            <v-card-title class="text-h5 grey lighten-2">
                Add a new item
            </v-card-title>
            <v-form v-model="valid" @submit.prevent="send" class="mx-1">
                <v-row>
                    <v-col>
                        <v-img :src="previewImage" class="d-flex" />
                        <input ref="fileselect" type="file" accept="image/jpeg" @change=uploadImage required>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <div class="d-flex justify-space-around align-center flex-column flex-md-row">
                            <v-text-field class="align-center" v-model="title" :rules="titleRules" label="Title"
                                density="compact" variant="outlined" style="width: auto" single-line hide-details
                                required>
                            </v-text-field>
                        </div>
                    </v-col>
                </v-row>
            </v-form>
            <v-card-actions>
                <v-spacer></v-spacer>
                <div class="d-flex justify-space-around align-center flex-column flex-md-row fill-height">
                    <v-btn class="ml-2" color="red darken-1" text @click="dialog = false" plain>
                        Cancel
                    </v-btn>
                    <v-btn class="ml-2" @click="send" :disabled="!valid" text plain>
                        Upload
                        <v-icon :color="(valid ? 'blue' : '')" icon="mdi-upload" />
                    </v-btn>
                </div>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { API_LOCATION } from "../config"

export default {
    
    name: 'ViewPost',

    props: {
        refresh: { type: Function }
    },

    data: () => ({
        valid: false,
        dialog: false,
        title: '',
        titleRules: [
            v => !!v || 'Title is required',
            v => (v && v.length <= 40) || 'Title must be less than 40 characters',
            v => !(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/).test(v) || 'Title must not contains special characters',
        ],
        previewImage: null
    }),

    methods: {
        send() {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: this.title, img: this.previewImage })
            };
            fetch(API_LOCATION+"/element", requestOptions)
            this.dialog = false
            this.refresh()
        },
        uploadImage(e) {
            const image = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(image);
            reader.onload = e => {
                this.previewImage = e.target.result;
                console.log(this.previewImage);
            };
        }
    },

    watch: {
        dialog: function (newValue, old) {
            if (!newValue && newValue != old) {
                this.title = ''
                this.previewImage = null
                this.refresh()
                //this.$refs.fileselect.reset();
            }
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
