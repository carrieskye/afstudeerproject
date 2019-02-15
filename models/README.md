# Pretrained models

This directory will contain pretrained models. Due to [limitiations of github](https://help.github.com/articles/working-with-large-files/) these could not be included in the repository but can be downloaded at:

- [yu4u/age-gender-estimation](https://github.com/yu4u/age-gender-estimation/releases)

## hashes of files to verify
```
$ find . -type f -size +100M -exec sha256sum {} \;
44e55457beed1659e66780da482d4d5a25f5f379ef92c0599fd1306d53882d8e  ./yu4u_age-gender-estimation/weights.28-3.73.hdf5
73cad6a9ec3fa1c01f3125711ccde8bb674f0a5f3e7631c14b4a196bd7831e0a  ./yu4u_age-gender-estimation/weights.29-3.76_utk.hdf5
8da393803358ff98089bef41d1bbd343e75536ccc79bd1667892be28c32c5a31  ./yu4u_age-gender-estimation/age_only_resnet50_weights.061-3.300-4.410.hdf5
```
