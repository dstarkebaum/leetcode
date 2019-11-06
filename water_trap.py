# https://leetcode.com/problems/trapping-rain-water/
#
# Solution by David Starkebaum 2019-11-05
# 
# Original thought process:
#
# move whichever pointer has a lower height forward...
#  (if the two are equal, move the left pointer.. doesn't really matter which)
#   while the left height is greater than or equal to the previous max,
#     update the left max height and move the left pointer forward
#   while the right height is greater than the right max:
#     update the right max height and move the right pointer forward
#   set the water level to the minimum of the left and right max
#   then compare the left and right max heights:
#
# if the height is lower than the water level:
#   calculate the difference and add to the total water volume
#
# if the height is greater than or equal to the water level:

def trap(self, height: List[int]) -> int:

    # can't trap any water with a terrain of length 2
    if len(height) < 3:
        return 0

    # two pointer solution:
    # left and right pointers start at either end
    left = 0
    right = len(height) - 1

    # doesn't really matter what I set these to at first
    # since I will update them inside the loop
    l_max = 0 # height[left]
    r_max = 0 # height[right]

    water_level = 0

    # the total volume of water trapped
    water_volume = 0


    # loop inward as long as the two don't cross
    # Note: be sure to include the case where left = right,
    #       or you will miss [2,0,2] --> 2!
    while left <= right:
        # optional print statement for debugging
        #print("[l, r, l_max, r_max, wl, wv] = ["+",".join(str(x) for x in
        #    [left,right,l_max,r_max,water_level, water_volume])+"]")

        # keep progressing the left pointer
        # and updating the max height on the left
        # so long as the height is flat or increasing
        if height[left] >= l_max:
            l_max = height[left]
            left += 1
            continue
        # same for the right side
        if height[right] >= r_max:
            r_max = height[right]
            right -= 1
            continue

        # now both the left and right pointer should have reached a point
        # where the height is less than their max!

        # the water level is determined by the lower of the two max heights
        water_level = min(l_max, r_max)

        # now start tallying up water_volume
        # as long as you are under the water level
        # Note: be sure to start from the side with the lower max height,
        # or you will miss [2,0,3,0,4] --> 5!
        if l_max <= r_max and height[left] < water_level:
            water_volume += water_level - height[left]
            left += 1
            continue

        if r_max <= l_max and height[right] < water_level:
            water_volume += water_level - height[right]
            right -= 1
            continue

    return water_volume
