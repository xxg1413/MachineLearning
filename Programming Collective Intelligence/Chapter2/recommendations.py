#coding=utf-8
from math import  sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


critics_chinese = {
                    '张三':{'伦敦陷落': 7.5, '火锅英雄': 8.5, '我的特工爷爷': 5.5,
                         '疯狂动物城': 9.1, '睡在我上铺的兄弟':6.5, '蝙蝠侠大战超人':8.5, '荒野猎人':9.5 },

                    '李四':{'伦敦陷落': 6.2, '火锅英雄': 9.3, '我的特工爷爷': 5.5,
                         '疯狂动物城': 8.9, '睡在我上铺的兄弟':7.0, '蝙蝠侠大战超人':8.9, '荒野猎人':7.9 },

                    '王五':{'伦敦陷落': 4.5, '火锅英雄': 7.7, '我的特工爷爷': 5.5,
                         '疯狂动物城': 9.7, '睡在我上铺的兄弟':6.6, '蝙蝠侠大战超人':7.8, '荒野猎人':9.1 },

                    '赵六':{'伦敦陷落': 6.5, '火锅英雄': 6.8, '我的特工爷爷': 5.5,
                         '疯狂动物城': 9.9, '睡在我上铺的兄弟':5.1, '蝙蝠侠大战超人':6.5, '荒野猎人':8.8 },

                    '齐七':{'伦敦陷落': 5.5, '火锅英雄': 9.0, '我的特工爷爷': 5.5,
                         '疯狂动物城': 8.5, '睡在我上铺的兄弟':6.1, '蝙蝠侠大战超人':6.2, '荒野猎人':8.5 },

                    '巴八':{'伦敦陷落': 8.5, '火锅英雄': 8.8, '我的特工爷爷': 5.5,
                         '疯狂动物城': 8.7, '睡在我上铺的兄弟':7.6, '蝙蝠侠大战超人':5.5, '荒野猎人':7.5 },

                    '玖九':{'伦敦陷落': 6.6, '火锅英雄': 6.9, '我的特工爷爷': 5.5,
                         '疯狂动物城': 9.9, '睡在我上铺的兄弟':5.5, '蝙蝠侠大战超人':7.9, '荒野猎人':7.7 },

                    '石十':{'伦敦陷落': 5.4, '火锅英雄': 7.5, '我的特工爷爷': 5.5,
                         '疯狂动物城': 9.5, '睡在我上铺的兄弟':4.5, '蝙蝠侠大战超人':8.5, '荒野猎人':9.1 }
                }


def sim_distance( prefs, p1, p2):
    si={}

    for i in prefs[p1]:
        if i in prefs[p2]:
            si[i] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum( [ pow([prefs[p1]][i] - prefs[p2][i], 2)
                          for i in prefs[p1] if i in prefs[p2] ]
                        )

    return 1 / (1 + sqrt(sum_of_squares))


if __name__ == "__main__":
    sim_distance(critics,'Lisa Rose', 'Gene Seymour')