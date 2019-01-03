import numpy as np
from math import *
from implicit_surface import *
from segment_surface import *

class Segment(object):
    def __init__(self, start, end, size):
        self.start = np.array(start)
        self.end = np.array(end)
        self.size = size

    def bbox(self):
        v_range = [None, None, None]
        for i in xrange(3):
            v_range[i] = [self.start[i],self.end[i]]
            if v_range[i][0] > v_range[i][1]:
                v_range[i] = [v_range[i][1],v_range[i][0]]
            v_range[i][0] -= self.size
            v_range[i][1] += self.size
        return np.array(v_range)

    def __repr__(self):
        return 'Segment('+repr(self.start)+','+repr(self.end)+','+repr(self.size)+')'


class Skeleton(object):
    def __init__(self, segments = []):
        self.segments = list(segments)

    def add_segment(self, p1, p2, size):
        self.segments.append(Segment(p1,p2,size))# append a new segment to self.segments

    def implicit_surface(self):
        """ Should return a blending function composed of SegmentImplicitSurface"""
        s = MinimumBlendingImplicitSurface()
        for seg in self.segments:
            segImpl = SegmentImplicitSurface(seg.start,seg.end,seg.size)
            s.add(segImpl)
        return s

    def bbox(self):
        s0 = self.segments[0]
        v_range = s0.bbox()
        for s in self.segments[1:]:
            v_rangei = s.bbox()
            for i in xrange(3):
                if v_range[i][0] > v_rangei[i][0]:
                    v_range[i][0] = v_rangei[i][0]
                if v_range[i][1] < v_rangei[i][1]:
                    v_range[i][1] = v_rangei[i][1]
        return v_range
    
    def __repr__(self):
        return 'Skeleton('+str(self.segments)+')'

    def write(self, fname):
        output = file(fname,'w')
        for s in self.segments:
            output.write('\t'.join(map(str,s.start))+'\t'+'\t'.join(map(str,p0))+'\t'+str(r)+'\n')

    def read(self, fname):
        import csv
        reader = csv.reader(open(filename,'r'),delimiter=' ')
        segments = []
        for line in reader:
            line = np.array(line).astype(float)
            segments.append(Segment(line[:3],line[3:6],line[-1]))
        self.segments = segments

