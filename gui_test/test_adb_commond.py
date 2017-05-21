#!/usr/bin/env python
# -*- coding:utf-8 -*-
import wx
import subprocess
# res = subprocess.Popen("adb shell ifconfig wlan0 | busybox awk 'NR==2{FS="[ :]+";print $4}'", shell=True).stdout.read()
# print res

# output=`dmesg | grep hda`
# becomes
# p1 = subprocess.Popen(["adb", "shell", "ifconfig", "wlan0"], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(["busybox", "awk", "'NR==2{FS="[ :]+";print $4}'"], stdin=p1.stdout, stdout=subprocess.PIPE)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
# output = p2.communicate()[0]
# print output

class AbstractList(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.ColumnSorterMixin):
    def __init__(self, parent, columes, editlabel=False):
        """list 控件封装 提供表头排序功能，建议使用"""
        wx.ListCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT | \
                             wx.SUNKEN_BORDER)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, len(columes))
        self.SetColumns(columes)
        self.ImageList = FileImageList()
        self.AssignImageList(self.ImageList, wx.IMAGE_LIST_SMALL)
        if editlabel:
            self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.EvtBeginEditLabel)
            self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.EvtEndEditLabel)
        self.pyData = ListPyData(self)
        self.itemDataMap = {}
        self.Bind(wx.EVT_RIGHT_DOWN, self.EvtContextMenu)

    def EvtContextMenu(self, evt):
        pMenu = self.InitPopuMenu()
        assert pMenu
        self.PopupMenu(pMenu)
        pMenu.Destroy()

    def InitPopuMenu(self):
        """init poup menu"""

    def EvtEndEditLabel(self, evt):
        """end edit label"""

    def EvtBeginEditLabel(self, evt):
        """begein edit label"""
        evt.Allow()

    def SetColumns(self, columes):
        """添加表头信息"""
        i = 0
        for name, width in columes:
            self.InsertColumn(i, name)
            if width:
                self.SetColumnWidth(i, width)
            else:
                self.setResizeColumn(i)
            i += 1

    def GetListCtrl(self):
        """这个方法只是为了表头排序"""
        return self

    def GetPyData(self, idx):
        return self.pyData.get(idx)

    def RemovePyData(self, idx):
        del self.pyData[idx]

    def RawIconAndRow(self, item):
        """格式化对象，添加到每一列中去"""
        NotImplemented('RawIconAndRow')

    def AddRow(self, item, idx=sys.maxint):
        icon, row = self.RawIconAndRow(item)
        idx = self.InsertImageStringItem(idx, row[0], icon)
        cols_num = len(row)
        for i in xrange(cols_num):
            self.SetStringItem(idx, i, row[i])
        self.pyData[idx] = item
        self.itemDataMap[idx] = row
        return idx

class AbstractControlList(AbstractList):
    def __init__(self, parent, columes, editlabel=False, style=wx.LC_REPORT):
        AbstractList.__init__(self, parent, columes, editlabel, False, style)

        self.Bind(wx.EVT_PAINT, self.PaintControl)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.PaintControl)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.PaintControl)
        self.Bind(wx.EVT_SCROLL, self.PaintControl)
        self.pyContol = ZipperMap()

    def RefreshColumText(self, rowidx):
        """refreshText of the list"""

    def PaintControl(self, evt):
        count = self.GetItemCount()
        for rowidx in xrange(count):
            pyData = self.GetPyData(rowidx)
            index_control = self.pyContol.get(id(pyData))
            if not index_control: continue
            for col, control in index_control:
                rect = self.GetCellRect(rowidx, col)
                control.SetDimensions(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2)
            self.RefreshColumText(rowidx)
        evt.Skip()

    def DeleteItem(self, idx):
        pyData = self.GetPyData(idx)
        assert pyData
        index_control = self.pyContol.get(id(pyData))
        if index_control:
            for col, control in index_control:
                self.__DropControl(control)
        AbstractList.DeleteItem(self, idx)

    def __DropControl(self, control):
        control.Hide()
        control.Destroy()
        del control

    def DeleteAllItems(self):
        for pyData in self.pyData.values():
            index_control = self.pyContol.get(id(pyData))
            if not index_control: continue
            for col, control in index_control:
                self.__DropControl(control)
            del self.pyContol[id(pyData)]
        AbstractList.DeleteAllItems(self)

    def RawIconAndRow(self, item):
        """格式化对象，添加到每一列中去"""
        NotImplemented('RawIconAndRow')

    def AddRow(self, item, idx=sys.maxint):
        icon, row = self.RawIconAndRow(item)
        idx = self.InsertImageStringItem(idx, row[0], icon)
        row_cout = len(row)
        for i in xrange(row_cout):
            if issubclass(type(row[i]), wx.Control):
                self.pyContol[id(item)] = i, row[i]
                row[i] = ''
            else:
                self.SetStringItem(idx, i, row[i])
        self.pyData[idx] = item
        self.itemDataMap[idx] = row
        return idx

    def _GetColumnWidthExtent(self, col):
        col_locs, loc = [0], 0
        num_cols = min(col + 1, self.GetColumnCount())
        for n in xrange(num_cols):
            loc += self.GetColumnWidth(n)
            col_locs.append(loc)
        x0 = col_locs[col]
        x1 = col_locs[col + 1] - 1
        return x0, x1

    def GetColumnRect(self, col):
        x0, x1 = self._GetColumnWidthExtent(col)
        r = self.GetItemRect(0)
        y0 = r.y
        y1 = self.GetClientSize()[1]
        x_scroll = self.GetScrollPos(wx.HORIZONTAL)
        return wx.RectPP(wx.Point(x0 - x_scroll, y0), wx.Point(x1 - x_scroll, y1))

    def GetCellRect(self, row, col):
        x0, x1 = self._GetColumnWidthExtent(col)
        r = self.GetItemRect(row)
        y0 = r.y
        y1 = r.GetBottom()
        x_scroll = self.GetScrollPos(wx.HORIZONTAL)
        return wx.RectPP(wx.Point(x0 - x_scroll, y0), wx.Point(x1 - x_scroll, y1))