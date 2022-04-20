<template>
  <div v-if="currentItem" class="edit-form py-3">
    <p class="headline">Edit Item</p>

    <v-form ref="form" lazy-validation>
      <v-text-field
        v-model="currentItem.name"
        :rules="[(v) => !!v || 'Title is required']"
        label="Title"
        required
      ></v-text-field>

      <v-text-field
        v-model="currentItem.description"
        :rules="[(v) => !!v || 'Description is required']"
        label="Description"
        required
      ></v-text-field>

      <!-- <label><strong>Status:</strong></label>
      {{ currentItem.published ? "Published" : "Pending" }} -->

      <!-- <v-divider class="my-5"></v-divider>

      <v-btn v-if="currentItem.published"
        @click="updatePublished(false)"
        color="primary" small class="mr-2"
      >
        UnPublish
      </v-btn> -->

      <!-- <v-btn v-else
        @click="updatePublished(true)"
        color="primary" small class="mr-2"
      >
        Publish
      </v-btn> -->

      <v-btn color="error" small class="mr-2" >
        Delete
      </v-btn>

      <v-btn color="success" small >
        Update
      </v-btn>
    </v-form>

    <p class="mt-3">{{ message }}</p>
  </div>

  <div v-else>
    <p>Please click on a Tutorial...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "tutorial",
  data() {
    return {
      currentItem: null,
      message: "",
    };
  },
  methods: {
    getItem(id) {
      const path = 'http://localhost:5000/api/item/'+ id;
      axios.get(path, )
        .then((res) => {
          this.currentItem = res.data;
          console.log(this.currentItem);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
  mounted() {
    this.message = "";
    this.getItem(this.$route.params.id);
    console.log(this.$route.params.id)
  }
};
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>
